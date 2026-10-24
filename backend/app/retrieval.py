"""Retrieval of passages for grounding: story articles + Wikipedia background."""

import json
import logging
import re

import httpx
from sklearn.feature_extraction.text import TfidfVectorizer

from . import db
from .config import USER_AGENT
from .ingest import extract_article
from .sources import SOURCE_MAP
from .textutil import chunk

log = logging.getLogger("finite.retrieval")
_wiki_cache: dict = {}


def story_articles(story, limit=4):
    ids = json.loads(story["article_ids"])
    arts = db.query(f"SELECT * FROM articles WHERE id IN ({','.join('?' * len(ids))})", ids)
    arts.sort(key=lambda a: -SOURCE_MAP.get(a["source_id"], {"weight": 0})["weight"])
    arts = arts[:limit]
    for a in arts:
        extract_article(a)
    return arts


def wiki_search(query: str, lang="en", limit=3):
    key = (query, lang, limit)
    if key in _wiki_cache:
        return _wiki_cache[key]
    api = f"https://{lang}.wikipedia.org/w/api.php"
    headers = {"User-Agent": USER_AGENT}
    pages = []
    try:
        r = httpx.get(api, params={"action": "query", "list": "search", "srsearch": query, "srlimit": limit, "format": "json"}, headers=headers, timeout=15)
        titles = [h["title"] for h in r.json().get("query", {}).get("search", [])]
        for t in titles:
            r = httpx.get(api, params={"action": "query", "prop": "extracts", "explaintext": 1, "exchars": 8000, "titles": t, "format": "json", "redirects": 1},
                          headers=headers, timeout=15)
            for p in r.json().get("query", {}).get("pages", {}).values():
                text = re.sub(r"\n=+ [^=]+ =+\n", "\n", p.get("extract", ""))
                if text:
                    pages.append({"title": p["title"], "url": f"https://{lang}.wikipedia.org/wiki/{p['title'].replace(' ', '_')}", "text": text})
    except Exception as e:
        log.info("wiki search failed for %r: %s", query, e)
    _wiki_cache[key] = pages
    return pages


def rank_passages(query: str, passages: list[dict], k: int):
    if not passages:
        return []
    texts = [query] + [p["text"] for p in passages]
    try:
        m = TfidfVectorizer(ngram_range=(1, 2), sublinear_tf=True).fit_transform(texts)
        sims = (m[1:] @ m[0].T).toarray().ravel()
    except ValueError:
        return passages[:k]
    order = sims.argsort()[::-1][:k]
    return [{**passages[i], "score": float(sims[i])} for i in order]


def gather(story, query: str, wiki_queries: list[str], k=10):
    """Return ranked passages with stable refs: A* for news articles, W* for Wikipedia."""
    passages = []
    for ai, a in enumerate(story_articles(story)):
        src = SOURCE_MAP.get(a["source_id"], {})
        for ci, text in enumerate(chunk(a["content"] or a["description"] or "")[:8]):
            passages.append({"ref": f"A{ai + 1}.{ci + 1}", "text": text, "kind": "news", "name": src.get("name", a["source_id"]),
                             "title": a["title"], "url": a["url"], "weight": src.get("weight", 0.5), "published_at": a["published_at"]})
    lang = "ml" if story["lang"] == "ml" and not any(re.search(r"[a-zA-Z]{3}", q) for q in wiki_queries) else "en"
    seen = set()
    wi = 0
    for q in wiki_queries[:3]:
        for page in wiki_search(q, lang, limit=2):
            if page["title"] in seen:
                continue
            seen.add(page["title"])
            wi += 1
            for ci, text in enumerate(chunk(page["text"])[:12]):
                passages.append({"ref": f"W{wi}.{ci + 1}", "text": text, "kind": "background", "name": "Wikipedia",
                                 "title": page["title"], "url": page["url"], "weight": 0.7})
    return rank_passages(query, passages, k)
