"""Ingestion: RSS discovery -> store -> classify into taxonomy. Full-text extraction happens lazily."""

import calendar
import concurrent.futures as cf
import json
import logging
import re
import time

import feedparser
import httpx
import trafilatura

from . import db, llm, linked_content
from .config import USER_AGENT
from .sources import SOURCE_MAP, SOURCES
from .taxonomy import STORY_TYPES, SUBFIELDS
from .textutil import clean_html, detect_lang, hid

log = logging.getLogger("finite.ingest")
HEADERS = {"User-Agent": USER_AGENT, "Accept-Language": "en-IN,en;q=0.9,ml;q=0.8"}

SOURCE_HINTS = {
    "lwn": {"open_source": 0.8}, "nasa": {"space": 0.8}, "techcrunch": {"startups": 0.5},
    "livemint_tech": {"electronics": 0.4}, "thehindu_kerala": {"kerala": 0.7}, "thehindu_business": {"companies": 0.3},
    "bbc_science": {"discoveries": 0.4}, "bbc_tech": {"ai": 0.2}, "altnews": {"internet_culture": 0.3},
    "mathrubhumi": {"kerala": 0.5}, "asianet": {"kerala": 0.5}, "twentyfour": {"kerala": 0.5}, "oneindia_ml": {"kerala": 0.5}, "gnews_ml": {"kerala": 0.5},
}
STORY_TYPE_WORDS = {k: set(v.split()) for k, v in STORY_TYPES.items()}
SUBFIELD_WORDS = {k: set(v["keywords"]) for k, v in SUBFIELDS.items()}


def _ts(entry, key):
    t = entry.get(key)
    return float(calendar.timegm(t)) if t else None


def fetch_feed(source):
    try:
        r = httpx.get(source["feed"], headers=HEADERS, timeout=20, follow_redirects=True)
        r.raise_for_status()
        feed = feedparser.parse(r.content)
    except Exception as e:
        log.warning("feed %s failed: %s", source["id"], e)
        return source["id"], []
    now = time.time()
    items = []
    for e in feed.entries[:80]:
        title, url = clean_html(e.get("title")), e.get("link")
        if not title or not url:
            continue
        desc = clean_html(e.get("summary") or e.get("description"))[:1500]
        lang = detect_lang(title + " " + desc)
        if lang == "other":
            continue
        published = _ts(e, "published_parsed") or _ts(e, "updated_parsed") or now
        updated = _ts(e, "updated_parsed") or published
        items.append({"id": hid(url), "source_id": source["id"], "lang": lang, "title": title, "url": url,
                      "description": desc, "published_at": min(published, now), "updated_at": min(max(updated, published), now), "fetched_at": now})
    return source["id"], items


def _terms(text):
    """Word set plus underscore-joined bigrams/trigrams so phrase keywords like 'supreme_court' match."""
    toks = re.findall(r"[a-z0-9][a-z0-9\-()]*", (text or "").lower())
    out = set(toks)
    out.update("_".join(toks[i:i + 2]) for i in range(len(toks) - 1))
    out.update("_".join(toks[i:i + 3]) for i in range(len(toks) - 2))
    return out


def keyword_classify(article):
    title_w, body_w = _terms(article["title"]), _terms(article.get("description", ""))
    scores = {}
    for sid, kws in SUBFIELD_WORDS.items():
        hits = 2 * len(title_w & kws) + len(body_w & kws)
        if hits >= 2:
            scores[sid] = min(1.0, hits / 4)
    for sid, w in SOURCE_HINTS.get(article["source_id"], {}).items():
        scores[sid] = max(scores.get(sid, 0), w)
    top = dict(sorted(scores.items(), key=lambda kv: -kv[1])[:3])
    st_scores = {k: 2 * len(title_w & v) + len(body_w & v) for k, v in STORY_TYPE_WORDS.items()}
    best = max(st_scores, key=st_scores.get)
    return top, best if st_scores[best] else "general"


LLM_CLASSIFY_SYSTEM = """You classify news headlines into a fixed taxonomy for an Indian news app.
Subfield ids: {subfields}
Story types: {types}, general
For each item return up to 3 subfield ids with relevance 0-1, and one story type.
Output: {{"items":[{{"i":<index>,"subfields":{{"<id>":<score>}},"type":"<story type>"}}]}}"""


def llm_classify(batch):
    system = LLM_CLASSIFY_SYSTEM.format(subfields=", ".join(SUBFIELDS), types=", ".join(STORY_TYPES))
    user = "\n".join(f'{i}. [{a["lang"]}] {a["title"]} — {(a.get("description") or "")[:200]}' for i, a in enumerate(batch))
    data = llm.chat_json(system, user)
    if not data:
        return None
    out = {}
    for it in data.get("items", []):
        i = it.get("i")
        if isinstance(i, int) and 0 <= i < len(batch):
            subs = {k: float(v) for k, v in (it.get("subfields") or {}).items() if k in SUBFIELDS}
            st = it.get("type") if it.get("type") in STORY_TYPES else "general"
            out[batch[i]["id"]] = (subs, st)
    return out


def classify_pending():
    rows = db.query("SELECT id, source_id, lang, title, description FROM articles WHERE classified=0")
    results = {}
    for i in range(0, len(rows), 40):
        batch = rows[i:i + 40]
        llm_out = llm_classify(batch) or {}
        for a in batch:
            kw_subs, kw_type = keyword_classify(a)
            subs, st = llm_out.get(a["id"], (None, None))
            results[a["id"]] = (subs or kw_subs, st or kw_type, 2 if a["id"] in llm_out else 1)
    with db.tx() as c:
        c.executemany("UPDATE articles SET subfields=?, story_type=?, classified=? WHERE id=?",
                      [(json.dumps(s), t, lvl, aid) for aid, (s, t, lvl) in results.items()])
    return len(results)


def run_ingest():
    t0 = time.time()
    new = 0
    with cf.ThreadPoolExecutor(12) as ex:
        for sid, items in ex.map(fetch_feed, SOURCES):
            with db.tx() as c:
                for a in items:
                    cur = c.execute(
                        """INSERT INTO articles(id,source_id,lang,title,url,description,published_at,updated_at,fetched_at)
                           VALUES(:id,:source_id,:lang,:title,:url,:description,:published_at,:updated_at,:fetched_at)
                           ON CONFLICT(id) DO UPDATE SET updated_at=MAX(articles.updated_at, excluded.updated_at), title=excluded.title""", a)
                    new += cur.rowcount
    classified = classify_pending()
    stats = {"at": time.time(), "articles_seen": new, "classified": classified, "seconds": round(time.time() - t0, 1)}
    db.kv_set("last_ingest", stats)
    log.info("ingest done %s", stats)
    return stats


def extract_article(article):
    """Fetch and extract full text for an article (cached in DB)."""
    if article["source_id"] == "hackernews":
        key = f"linked-content-v{linked_content.VERSION}:" + article["id"]
        info = db.kv_get(key)
        if not info or (info.get("status") == "unavailable" and time.time() - info.get("checked_at", 0) > 3600):
            info = linked_content.resolve(article)
            db.kv_set(key, info)
        if info["url"].startswith("https://gitlab.com/") and info["content"]:
            info["content"] = linked_content.readme_prose(info["content"])
            db.kv_set(key, info)
        article["content"] = info["content"]
        article["description"] = ""  # Discovery metadata must never become evidence.
        article["url"] = info["url"]
        article["discussion_url"] = info.get("discussion_url")
        with db.tx() as c:
            c.execute("UPDATE articles SET content=? WHERE id=?", (info["content"], article["id"]))
        return info["content"]
    if article.get("content"):
        return article["content"]
    text = ""
    if SOURCE_MAP.get(article["source_id"], {}).get("extract", True):
        try:
            r = httpx.get(article["url"], headers=HEADERS, timeout=20, follow_redirects=True)
            if r.status_code == 200:
                text = trafilatura.extract(r.text, include_comments=False, include_tables=False, favor_precision=True) or ""
        except Exception as e:
            log.info("extract failed %s: %s", article["url"], e)
    text = text.strip() or article.get("description") or ""
    with db.tx() as c:
        c.execute("UPDATE articles SET content=? WHERE id=?", (text[:20000], article["id"]))
    article["content"] = text
    return text
