"""Rabbit holes: grounded, cited, depth-limited explorations. Generated once per (story, question) and shared."""

import json
import re
import time

from . import db, llm
from .analysis import ANGLES, analyze, proper_nouns
from .config import FAST_MODEL, MAX_DEPTH, MOCK_MODE, SMART_MODEL
from .retrieval import gather
from .textutil import hid, sentences, words

YEAR_RE = re.compile(r"\b(1[5-9]\d\d|20[0-4]\d)\b")

SYNTH_SYSTEM = """You write one step of a "rabbit hole" for Finite, a news app that explains how stories came to be.
You get a news story, a reader's question, and numbered passages (refs like A1.2 = news article, W1.3 = Wikipedia background).
Rules:
- Use ONLY the passages. Every node must cite the passage refs that support it. No outside knowledge.
- If the passages cannot answer the question, set "insufficient": true and return the few things they do support.
- If the question is unrelated to the story, set "off_topic": true and return no nodes.
- Separate fact from claim: confidence is "verified" (established fact), "reported" (one source says), or "disputed" (sources disagree / contested claim).
- Do not create false balance: if evidence favours one account, say so.
- Keep it calm, clear and concrete. 2-4 nodes, each 2-4 sentences.
Output JSON:
{"title": short title for this step,
 "nodes": [{"heading": str, "text": str, "citations": ["A1.2", ...], "confidence": "verified|reported|disputed"}],
 "timeline": [{"date": str, "event": str, "citations": [...]}]   // only for origin/history-type questions, chronological, may be empty,
 "next_questions": [{"question": str, "angle": "connection|history|mechanism|parallel|impact", "search": [1-2 English Wikipedia queries]}]  // 2-3 deeper "connection" questions (broader ideas, historical parallels, principles, institutions); [] if told this is the final level,
 "concepts": [2-4 Wikipedia article names learned in this step],
 "insufficient": bool, "off_topic": bool}"""

VERIFY_SYSTEM = """You are a strict fact-checker. For each numbered claim, decide whether the cited passages directly support it.
Output {"results": [{"i": <index>, "supported": true|false}]}"""


def _key(story_id, question, lang):
    return hid(story_id, re.sub(r"[^a-z0-9\u0D00-\u0D7F ]", "", question.lower()).strip(), lang)


def _verify(nodes, passages):
    if not nodes:
        return [], 0
    by_ref = {p["ref"]: p["text"] for p in passages}
    claims = "\n\n".join(f"{i}. CLAIM: {n['text']}\nPASSAGES: " + " | ".join(by_ref.get(r, "")[:2000] for r in n["citations"]) for i, n in enumerate(nodes))
    data = llm.chat_json(VERIFY_SYSTEM, claims, model=FAST_MODEL)
    verdicts = data.get("results", []) if isinstance(data, dict) else []
    accepted = []
    if isinstance(verdicts, list):
        for i, node in enumerate(nodes):
            matches = [v for v in verdicts if isinstance(v, dict) and type(v.get("i")) is int and v["i"] == i]
            if len(matches) == 1 and matches[0].get("supported") is True:
                accepted.append(node)
    return accepted, len(nodes) - len(accepted)


def _extractive(question, angle, passages, depth, concepts):
    qw = words(question)
    nodes = []
    for p in passages[:4]:
        sents = sentences(p["text"]) or [p["text"]]
        sents.sort(key=lambda s: -len(words(s) & qw))
        nodes.append({"heading": p["title"], "text": " ".join(sents[:2]), "citations": [p["ref"]],
                      "confidence": "reported"})
    timeline = []
    if angle in {"origin", "history", "prior_work", "precedent", "connection"}:
        for p in passages:
            for s in sentences(p["text"]):
                m = YEAR_RE.search(s)
                if m and len(timeline) < 6:
                    timeline.append({"date": m.group(1), "event": s[:220], "citations": [p["ref"]]})
        timeline.sort(key=lambda t: t["date"])
    found = proper_nouns(" ".join(p["text"] for p in passages), 6)
    nxt = []  # Capitalized names alone do not establish a meaningful follow-up.
    return {"title": question, "nodes": nodes, "timeline": timeline, "next_questions": nxt, "concepts": found[:4], "insufficient": True, "off_topic": False}


def explore(story_id, question: str, angle: str = "context", search: list[str] | None = None, depth: int = 1, custom: bool = False, path: list | None = None):
    depth = max(1, min(MAX_DEPTH, depth))
    # Version the cache by depth and retrieval inputs so final-level responses stay final.
    key = hid("explore-v4", str(MOCK_MODE), FAST_MODEL, SMART_MODEL, _key(story_id, question, "en"), str(depth), angle,
              json.dumps(search or [], ensure_ascii=False), str(custom))
    cached = db.query("SELECT payload FROM explorations WHERE key=?", (key,))
    if cached:
        payload = json.loads(cached[0]["payload"])
        if MOCK_MODE or payload.get("mode") == "ai":
            return {**payload, "path": path or []}
    story = db.query("SELECT * FROM stories WHERE id=?", (story_id,))
    if not story:
        return None
    story = story[0]
    analysis = analyze(story_id)
    concepts = analysis.get("concepts", [])
    queries = [q for q in (search or []) if q] or [question + " " + " ".join(concepts[:1])] + concepts[:1]

    if custom:
        story_words = words(story["title"] + " " + analysis["summary"]["deep"] + " " + " ".join(concepts))
        if MOCK_MODE and not (words(question) & story_words):
            return {"key": key, "question": question, "off_topic": True, "nodes": [], "depth": depth}

    passages = gather(story, f"{question} {story['title']}", queries, k=10)
    final = depth >= MAX_DEPTH
    user = (f"STORY: {story['title']}\nSUMMARY: {analysis['summary']['standard']}\n"
            f"READER QUESTION: {question}\nANGLE: {angle}\nLEVEL: {depth} of {MAX_DEPTH}{' (final level: next_questions must be [])' if final else ''}\n\nPASSAGES:\n" +
            "\n\n".join(f"[{p['ref']}] ({p['name']}: {p['title']})\n{p['text']}" for p in passages))
    data = llm.chat_json(SYNTH_SYSTEM, user, model=SMART_MODEL)
    dropped = 0
    if data and isinstance(data.get("nodes"), list):
        refs = {p["ref"] for p in passages}
        nodes = [{**n, "citations": [r for r in n.get("citations", []) if isinstance(r, str) and r in refs]} for n in data["nodes"] if isinstance(n, dict) and isinstance(n.get("text"), str) and isinstance(n.get("citations"), list)]
        uncited = sum(1 for n in nodes if not n["citations"])
        nodes = [n for n in nodes if n["citations"]]
        nodes, dropped = _verify(nodes, passages)
        dropped += uncited
        for node in nodes:
            node["heading"] = str(node.get("heading") or "Source-backed context")
            if node.get("confidence") not in {"reported", "disputed"}:
                node["confidence"] = "reported"
        data["nodes"] = nodes
        timeline = [{**t, "text": f"{t.get('date', '')}: {t['event']}", "citations": [r for r in (t.get("citations") if isinstance(t.get("citations"), list) else []) if isinstance(r, str) and r in refs]}
                    for t in (data.get("timeline") if isinstance(data.get("timeline"), list) else []) if isinstance(t, dict) and isinstance(t.get("event"), str)]
        timeline = [t for t in timeline if t["citations"]]
        timeline, timeline_dropped = _verify(timeline, passages)
        dropped += timeline_dropped
        data["timeline"] = [{k: v for k, v in t.items() if k != "text"} for t in timeline]
        if not nodes:
            data["insufficient"] = True
        data["next_questions"] = [] if final or not nodes else [q for q in data.get("next_questions", []) if isinstance(q, dict) and isinstance(q.get("question"), str) and isinstance(q.get("angle"), str) and isinstance(q.get("search", []), list) and all(isinstance(x, str) for x in q.get("search", []))][:3] if isinstance(data.get("next_questions", []), list) else []
        data["concepts"] = [c for c in data.get("concepts", []) if isinstance(c, str)][:6] if isinstance(data.get("concepts", []), list) else []
        data["mode"] = "ai"
    else:
        data = _extractive(question, angle, passages, depth, concepts)
        data["mode"] = "extractive"

    used = {r for n in data["nodes"] for r in n["citations"]} | {r for t in data.get("timeline", []) for r in t["citations"]}
    data.update({
        "key": key, "story_id": story_id, "question": question, "angle": angle, "depth": depth, "max_depth": MAX_DEPTH, "custom": custom,
        "dropped_claims": dropped, "path": path or [],
        "sources": {p["ref"]: {k: p.get(k) for k in ("kind", "name", "title", "url", "weight")} for p in passages if p["ref"] in used},
        "created_at": time.time(),
    })
    if not data.get("off_topic"):
        with db.tx() as c:
            c.execute("INSERT OR REPLACE INTO explorations(key, story_id, payload, created_at) VALUES(?,?,?,?)",
                      (key, story_id, json.dumps(data, ensure_ascii=False), time.time()))
    return data


def angle_label(angle):
    return ANGLES.get(angle, (angle, ""))[0]
