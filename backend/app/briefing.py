"""Briefing builder: lookback window -> dedupe vs previous briefings -> cluster -> weighted rank -> freeze."""

import json
import math
import time
from collections import Counter

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

from . import db, llm
from .sources import SOURCE_MAP
from .taxonomy import SUBFIELDS
from .textutil import hid

PRIORITY_WEIGHT = {3: 1.0, 2: 0.6, 1: 0.3}

DEFAULT_PROFILE = {
    "onboarded": False,
    "languages": ["en"],
    "ui_language": "en",
    "interests": {},  # subfield_id -> priority 1..3
    "excluded_subfields": [],
    "excluded_sources": [],
    "delivery_time": "07:30",
    "timezone": "Asia/Kolkata",
    "lookback_hours": 30,
    "stories_per_briefing": 12,
    "depth": "standard",
}


def get_profile(user_id=None):
    return {**DEFAULT_PROFILE, **(db.kv_get(f"profile:{user_id}" if user_id is not None else "profile") or {})}


def save_profile(p, user_id=None):
    p = {**get_profile(user_id), **p}
    p["interests"] = {k: int(v) for k, v in p["interests"].items() if k in SUBFIELDS and int(v) in PRIORITY_WEIGHT}
    p["lookback_hours"] = max(6, min(72, int(p["lookback_hours"])))
    p["stories_per_briefing"] = max(3, min(25, int(p["stories_per_briefing"])))
    if "en" not in p["languages"]:
        p["languages"] = ["en", *p["languages"]]
    db.kv_set(f"profile:{user_id}" if user_id is not None else "profile", p)
    return p


def _relevance(subs, profile):
    excluded = set(profile["excluded_subfields"])
    if subs and max(subs, key=subs.get) in excluded:
        return 0.0, None
    best, best_sid = 0.0, None
    for sid, conf in subs.items():
        w = PRIORITY_WEIGHT.get(profile["interests"].get(sid, 0), 0)
        if w * conf > best:
            best, best_sid = w * conf, sid
    return best, best_sid


def _cluster(arts):
    """Greedy clustering on similarity. Uses embeddings when available, TF-IDF otherwise."""
    texts = [a["title"] + ". " + (a.get("description") or "")[:300] for a in arts]
    vecs = llm.embed(texts)
    if vecs:
        m = np.array(vecs)
        m /= np.linalg.norm(m, axis=1, keepdims=True) + 1e-9
        sim, thresh = m @ m.T, 0.8
    else:
        m = TfidfVectorizer(stop_words="english", ngram_range=(1, 2), min_df=1, sublinear_tf=True).fit_transform(texts)
        sim, thresh = (m @ m.T).toarray(), 0.32
    order = sorted(range(len(arts)), key=lambda i: -arts[i]["_score"])
    assigned, clusters = set(), []
    for i in order:
        if i in assigned:
            continue
        members = [j for j in np.where(sim[i] >= thresh)[0] if j not in assigned and (vecs or arts[j]["lang"] == arts[i]["lang"])]
        if i not in members:
            members.insert(0, i)
        assigned.update(members)
        clusters.append([arts[j] for j in members])
    return clusters


def build_briefing(profile=None, user_id=None, edition_of=None, scheduled_for=None):
    profile = profile or get_profile(user_id)
    now = time.time()
    start = now - profile["lookback_hours"] * 3600
    excluded_src = set(profile["excluded_sources"])
    langs = set(profile["languages"])

    prev_ids = set()
    for b in db.query("SELECT story_ids FROM briefings WHERE user_id IS ?", (user_id,)):
        for sid in json.loads(b["story_ids"]):
            for s in db.query("SELECT article_ids FROM stories WHERE id=?", (sid,)):
                prev_ids.update(json.loads(s["article_ids"]))

    rows = db.query("SELECT id, source_id, lang, title, url, description, published_at, updated_at, subfields, story_type FROM articles "
                    "WHERE published_at >= ? AND classified > 0", (start,))
    arts = []
    for a in rows:
        if a["source_id"] in excluded_src or a["lang"] not in langs or a["source_id"] not in SOURCE_MAP:
            continue
        a["subfields"] = json.loads(a["subfields"] or "{}")
        rel, sid = _relevance(a["subfields"], profile)
        if rel <= 0:
            continue
        hours = (now - a["published_at"]) / 3600
        a["_score"] = rel * (0.5 + 0.5 * SOURCE_MAP[a["source_id"]]["weight"]) * math.exp(-hours / 26)
        a["_sid"] = sid
        arts.append(a)
    if not arts:
        return None

    scored = []
    for cl in _cluster(arts):
        ids = [a["id"] for a in cl]
        if sum(i in prev_ids for i in ids) > len(ids) / 2:
            continue
        sources = {a["source_id"] for a in cl}
        tiers = {SOURCE_MAP[s]["tier"] for s in sources}
        coverage = 1 + 0.3 * math.log2(len(sources))
        penalty = 0.6 if tiers == {"aggregator"} else 1.0
        score = max(a["_score"] for a in cl) * coverage * penalty
        scored.append((score, cl))
    scored.sort(key=lambda x: -x[0])

    n = profile["stories_per_briefing"]
    cap = max(2, math.ceil(n / 4))
    per_sub, chosen = Counter(), []
    for score, cl in scored:
        lead = max(cl, key=lambda a: a["_score"])
        if per_sub[lead["_sid"]] >= cap:
            continue
        per_sub[lead["_sid"]] += 1
        chosen.append((score, cl, lead))
        if len(chosen) >= n:
            break

    if not chosen:
        return None
    story_ids = []
    with db.tx() as c:
        for score, cl, lead in chosen:
            cl.sort(key=lambda a: -SOURCE_MAP[a["source_id"]]["weight"])
            rep = next((a for a in cl if a["lang"] == profile["ui_language"]), cl[0])
            subs = Counter()
            for a in cl:
                for k, v in a["subfields"].items():
                    subs[k] = max(subs[k], v)
            sid = "s" + hid(*sorted(a["id"] for a in cl))
            st = Counter(a["story_type"] for a in cl).most_common(1)[0][0]
            c.execute("""INSERT INTO stories(id, article_ids, title, lang, subfields, story_type, created_at)
                         VALUES(?,?,?,?,?,?,?) ON CONFLICT(id) DO NOTHING""",
                      (sid, json.dumps([a["id"] for a in cl]), rep["title"], rep["lang"], json.dumps(dict(subs.most_common(3))), st, now))
            story_ids.append(sid)
        cur = c.execute("INSERT INTO briefings(created_at, window_start, window_end, config, story_ids, user_id, edition_of, scheduled_for) VALUES(?,?,?,?,?,?,?,?)",
                        (now, start, now, json.dumps(profile), json.dumps(story_ids), user_id, edition_of, scheduled_for))
        bid = cur.lastrowid
    return bid


def briefing_payload(bid, user_id=None):
    rows = db.query("SELECT * FROM briefings WHERE id=? AND user_id IS ?", (bid, user_id))
    if not rows:
        return None
    b = rows[0]
    story_ids = json.loads(b["story_ids"])
    stories = []
    for sid in story_ids:
        s = db.query("SELECT * FROM stories WHERE id=?", (sid,))
        if s:
            stories.append(story_card(s[0]))
    return {"id": b["id"], "created_at": b["created_at"], "window_start": b["window_start"], "window_end": b["window_end"],
            "can_refresh": not b["refresh_used"] and b["edition_of"] is None, "edition_of": b["edition_of"],
            "config": json.loads(b["config"]), "stories": stories, "read_ids": json.loads(b["read_ids"]), "completed_at": b["completed_at"]}


def story_card(s):
    ids = json.loads(s["article_ids"])
    arts = db.query(f"SELECT id, source_id, title, url, published_at, updated_at, description FROM articles WHERE id IN ({','.join('?' * len(ids))})", ids)
    arts.sort(key=lambda a: -SOURCE_MAP.get(a["source_id"], {"weight": 0})["weight"])
    analysis = json.loads(s["analysis"]) if s["analysis"] else None
    subs = json.loads(s["subfields"])
    return {
        "id": s["id"], "title": s["title"], "lang": s["lang"], "story_type": s["story_type"],
        "subfields": [{"id": k, "name": SUBFIELDS[k]["name"], "score": v} for k, v in subs.items() if k in SUBFIELDS],
        "published_at": min(a["published_at"] for a in arts) if arts else s["created_at"],
        "updated_at": max(a["updated_at"] for a in arts) if arts else s["created_at"],
        "sources": [{"id": a["source_id"], "name": SOURCE_MAP[a["source_id"]]["name"], "tier": SOURCE_MAP[a["source_id"]]["tier"],
                     "weight": SOURCE_MAP[a["source_id"]]["weight"], "url": a["url"], "title": a["title"]} for a in arts if a["source_id"] in SOURCE_MAP],
        "teaser": (analysis or {}).get("summary", {}).get("quick") or (arts[0]["description"][:240] if arts and arts[0]["description"] else ""),
        "analyzed": bool(analysis),
    }


def mark_read(bid, story_id, user_id=None):
    rows = db.query("SELECT story_ids, read_ids FROM briefings WHERE id=? AND user_id IS ?", (bid, user_id))
    if not rows:
        return None
    read = set(json.loads(rows[0]["read_ids"]))
    if story_id not in json.loads(rows[0]["story_ids"]):
        return None
    read.add(story_id)
    all_ids = set(json.loads(rows[0]["story_ids"]))
    completed = time.time() if all_ids <= read else None
    with db.tx() as c:
        c.execute("UPDATE briefings SET read_ids=?, completed_at=COALESCE(completed_at, ?) WHERE id=?", (json.dumps(sorted(read)), completed, bid))
    return briefing_payload(bid, user_id)


def list_briefings(user_id, before=None, limit=20):
    rows = db.query("SELECT * FROM briefings WHERE user_id=? AND (? IS NULL OR id<?) ORDER BY id DESC LIMIT ?", (user_id, before, before, limit + 1))
    items = []
    for b in rows[:limit]:
        ids = json.loads(b['story_ids'])
        title = db.query('SELECT title FROM stories WHERE id=?', (ids[0],)) if ids else []
        items.append({'id': b['id'], 'created_at': b['created_at'], 'story_count': len(ids),
                      'read_count': len(json.loads(b['read_ids'])), 'completed_at': b['completed_at'],
                      'can_refresh': not b['refresh_used'] and b['edition_of'] is None, 'edition_of': b['edition_of'],
                      'headline': title[0]['title'] if title else 'No stories in this edition'})
    return {'items': items, 'next_cursor': items[-1]['id'] if len(rows) > limit else None}
