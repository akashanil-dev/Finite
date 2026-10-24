"""Story analysis: layered summaries, verified facts, the Missing Piece and story-specific rabbit-hole questions."""

import json
import re
from collections import Counter

from . import db, llm
from .config import FAST_MODEL, MOCK_MODE
from .retrieval import story_articles
from .sources import SOURCE_MAP
from .textutil import sentences

ANGLES = {
    "origin": ("How did this begin?", "Trace the events that led here"),
    "stakeholders": ("Who is involved?", "The groups involved and their positions"),
    "dispute": ("What exactly is being disputed?", "The claims on each side"),
    "place": ("Why here?", "The place and its history"),
    "next": ("What could happen next?", "Possible outcomes and what to watch"),
    "problem": ("What problem is this meant to solve?", "The issue behind the decision"),
    "evidence": ("What evidence supports it?", "Data and research behind the claims"),
    "stakes": ("What is at stake?", "Why this matters and for whom"),
    "history": ("How did we get here?", "The longer history behind the story"),
    "case": ("What is the case about?", "The facts and parties"),
    "law": ("Which law is involved?", "The legal framework"),
    "precedent": ("Has this happened before?", "Earlier cases and parallels"),
    "impact": ("Who does this affect?", "Consequences for people and institutions"),
    "mechanism": ("How does it work?", "The technology or mechanism explained"),
    "prior_work": ("What came before this?", "Earlier experiments and breakthroughs"),
    "competition": ("Who else is doing this?", "Rivals and alternatives"),
    "protect": ("How can people protect themselves?", "Practical defences"),
    "why_moved": ("Why did this move?", "The forces behind the change"),
    "why_here": ("Why did it happen here?", "Geography, conditions and risk"),
    "response": ("How are authorities responding?", "Relief, rescue and accountability"),
    "prevention": ("Could it have been prevented?", "Warnings, preparedness and lessons"),
    "context": ("What is the background?", "Context that the headline leaves out"),
    "why_matters": ("Why does this matter?", "The bigger picture"),
}

TYPE_ANGLES = {
    "general": ["context", "origin", "stakeholders", "why_matters", "next"],
    "policy": ["problem", "origin", "stakeholders", "evidence", "next"],
    "protest": ["origin", "stakeholders", "dispute", "place", "next"],
    "election": ["stakes", "history", "stakeholders", "next"],
    "court": ["case", "law", "precedent", "impact", "next"],
    "space": ["mechanism", "history", "stakeholders", "next"],
    "science": ["mechanism", "prior_work", "evidence", "impact"],
    "tech_product": ["mechanism", "history", "competition", "impact"],
    "security": ["mechanism", "impact", "history", "protect"],
    "markets": ["why_moved", "history", "impact", "next"],
    "economy": ["mechanism", "history", "impact", "next"],
    "disaster": ["why_here", "history", "response", "prevention"],
    "conflict": ["origin", "stakeholders", "history", "next"],
    "diplomacy": ["stakes", "history", "stakeholders", "next"],
    "crime": ["context", "law", "next"],
    "sports": ["stakes", "history", "next"],
    "culture": ["context", "history", "impact"],
    "health": ["mechanism", "history", "impact", "prevention"],
}

MISSING_TEMPLATES = {
    "policy": ["What problem is the policy intended to solve?", "What evidence supports the proposed solution?", "Who is likely to be affected?", "What remains uncertain?"],
    "protest": ["What specific change are the protesters asking for?", "What has the government said in response?", "How long has this dispute been building?"],
    "court": ["What did the lower courts decide?", "Which law or constitutional provision is in question?", "What happens to the parties now?"],
    "default": ["What led up to this?", "Who is affected, and how?", "What is still unconfirmed?"],
}

STOP_CAPS = {"The", "A", "An", "In", "On", "At", "This", "That", "He", "She", "It", "They", "We", "I", "But", "And", "Also", "However", "Monday", "Tuesday",
             "Wednesday", "Thursday", "Friday", "Saturday", "Sunday", "January", "February", "March", "April", "May", "June", "July", "August",
             "September", "October", "November", "December", "Mr", "Ms", "Dr", "PTI", "IANS", "ANI", "Photo", "Read", "Also Read"}


def proper_nouns(text, k=6):
    phrases = re.findall(r"\b([A-Z][a-zA-Z\-]+(?:\s+(?:of|the|and|de)?\s*[A-Z][a-zA-Z\-]+){0,3})", text)
    c = Counter(p.strip() for p in phrases if p.split()[0] not in STOP_CAPS and len(p) > 3)
    return [p for p, _ in c.most_common(k)]


def _refs(arts):
    return [{"ref": f"A{i + 1}", "source": SOURCE_MAP.get(a["source_id"], {}).get("name", a["source_id"]), "title": a["title"], "url": a["url"],
             "tier": SOURCE_MAP.get(a["source_id"], {}).get("tier"), "weight": SOURCE_MAP.get(a["source_id"], {}).get("weight", 0.5),
             "published_at": a["published_at"], "updated_at": a["updated_at"]} for i, a in enumerate(arts)]


def _questions_from_angles(angles, concepts):
    out = []
    for i, ang in enumerate(angles):
        q, blurb = ANGLES[ang]
        out.append({"id": f"q{i + 1}", "question": q, "angle": ang, "blurb": blurb, "search": concepts[:2] if concepts else []})
    return out


def _extractive(story, arts):
    texts = [a["content"] or a["description"] or "" for a in arts]
    texts = texts or [story["title"]]
    lead = sentences(texts[0]) or [texts[0][:300]]
    allsents = [(i, s) for i, t in enumerate(texts) for s in sentences(t)[:6]]
    concepts = proper_nouns(" ".join(texts))
    st = story["story_type"] or "general"
    facts = [{"text": s, "citations": [f"A{i + 1}"]} for i, s in allsents[:4]]
    return {
        "summary": {"quick": lead[0][:300], "standard": " ".join(lead[:3]), "deep": " ".join(s for _, s in allsents[:8])},
        "what_happened": facts,
        "missing_piece": [{"question": q, "why": "Not addressed in the coverage we found."} for q in MISSING_TEMPLATES.get(st, MISSING_TEMPLATES["default"])],
        "questions": _questions_from_angles(TYPE_ANGLES.get(st, TYPE_ANGLES["general"]), concepts),
        "concepts": concepts,
        "story_type": st,
        "mode": "extractive",
    }


ANALYSIS_SYSTEM = """You are the editor of Finite, a calm, finite news app that helps readers understand stories, not just skim them.
You receive several news articles (refs A1..An) about the same event. Using ONLY these articles:
1. summary: {"quick": 1-2 sentences (~30s read), "standard": ~120 words (~2 min), "deep": ~350 words (~5 min) covering context and significance}.
2. what_happened: 3-6 verified key facts, each {"text", "citations": ["A1", ...]}. Only facts stated in the articles. Note disagreements between sources.
3. story_type: one of policy, protest, election, court, space, science, tech_product, security, markets, economy, disaster, conflict, diplomacy, crime, sports, culture, health, general.
4. missing_piece: 3-4 important questions the coverage does NOT answer, each {"question", "why": why it matters}. This is "what the news didn't explain".
5. questions: 4-6 rabbit-hole questions tailored to THIS story, each {"id": "q1".., "question": short and specific, "angle": one of origin, stakeholders, dispute, place, next, problem, evidence, stakes, history, case, law, precedent, impact, mechanism, prior_work, competition, why_moved, why_here, response, prevention, context, why_matters, "blurb": <= 8 words, "search": 1-3 Wikipedia search queries (English) that would find background}. Prefer questions that fill the missing pieces. Questions must be answerable with background research.
6. concepts: 3-6 durable knowledge concepts a reader would learn about (Wikipedia article names, e.g. "Jantar Mantar", "Orbital mechanics").
Be neutral and precise. Never invent facts. Write in English."""


def analyze(story_id):
    rows = db.query("SELECT * FROM stories WHERE id=?", (story_id,))
    if not rows:
        return None
    story = rows[0]
    if story["analysis"]:
        cached = json.loads(story["analysis"])
        if MOCK_MODE or cached.get("mode") == "ai":
            return cached
    arts = story_articles(story)
    refs = _refs(arts)
    user = "\n\n".join(f"[A{i + 1}] {r['source']} — {a['title']}\n{(a['content'] or a['description'] or '')[:3500]}" for i, (a, r) in enumerate(zip(arts, refs)))
    data = llm.chat_json(ANALYSIS_SYSTEM, user, model=FAST_MODEL)
    if data and data.get("summary") and data.get("questions"):
        data["mode"] = "ai"
        data["story_type"] = data.get("story_type") or story["story_type"]
        data["questions"] = [{**q, "id": f"q{i + 1}"} for i, q in enumerate(data["questions"][:6]) if q.get("question")]
    else:
        data = _extractive(story, arts)
    data["articles"] = refs
    with db.tx() as c:
        c.execute("UPDATE stories SET analysis=?, story_type=? WHERE id=?", (json.dumps(data, ensure_ascii=False), data["story_type"], story_id))
    return data
