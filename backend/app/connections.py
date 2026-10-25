"""Finite cross-story comparisons using literal source evidence, never generated links."""
import json
import re

from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS
from .analysis import proper_nouns

from . import briefing, db
from .sources import SOURCE_MAP
from .textutil import SENT_RE

MAX_CONNECTIONS = 3
MAX_CANDIDATES = 200
# Extractive concepts sometimes contain sentence starters or generic roles.
GENERIC = {'after', 'before', 'during', 'according', 'considering', 'story', 'union',
           'police', 'protesters', 'chief minister', 'government', 'india', 'news',
           'responding', 'subsequently', 'reportedly', 'meanwhile', 'said', 'says',
           'latest', 'new', 'report', 'reports', 'today', 'yesterday'} | set(ENGLISH_STOP_WORDS)


def _terms(text):
    return {w for w in re.findall(r'[^\W\d_]+', text.casefold()) if len(w) > 2 and w not in GENERIC}


def _concepts(story, articles):
    analysis = json.loads(story['analysis'] or '{}')
    values = analysis.get('concepts', [])
    if not isinstance(values, list):
        values = []
    # Revalidate cached concepts; derive title entities even for old bad analyses.
    values = [*proper_nouns(' '.join(a['title'] for a in articles), 30), *values]
    seen, result = set(), []
    for value in values:
        if not isinstance(value, str):
            continue
        value = re.sub(r"\s+(?:VC|V-C|CEO|Chairman|President|Director)$", "", value.strip())
        key = value.casefold()
        if 3 <= len(value) <= 80 and key not in seen and _terms(value) and key not in GENERIC:
            seen.add(key)
            result.append(value)
    return result[:30]


def _evidence(articles, concept, title_only=False):
    pattern = re.compile(r'(?<!\w)' + re.escape(concept) + r'(?!\w)', re.IGNORECASE)
    for article in articles:
        passages = [article['title']] if title_only else [article['title'], *SENT_RE.split(article.get('content') or article.get('description') or '')]
        for passage in passages:
            passage = passage.strip()
            if 10 <= len(passage) <= 600 and pattern.search(passage):
                source = SOURCE_MAP.get(article['source_id'], {})
                return {'text': passage, 'name': source.get('name', article['source_id']),
                        'title': article['title'], 'url': article['url'], 'weight': source.get('weight', 0), 'kind': 'article'}
    return None


def explore(story_id, user_id=None):
    rows = db.query('SELECT * FROM stories WHERE id=?', (story_id,))
    if not rows:
        return None
    origin = rows[0]
    profile = briefing.get_profile(user_id)
    excluded = set(profile['excluded_sources'])

    def articles(story):
        ids = json.loads(story['article_ids'])
        rows = db.query(f"SELECT * FROM articles WHERE id IN ({','.join('?' for _ in ids)}) ORDER BY id", ids) if ids else []
        return [a for a in rows if a['source_id'] not in excluded]

    origin_articles = articles(origin)
    origin_ids = set(json.loads(origin['article_ids']))
    origin_urls = {a['url'] for a in origin_articles}
    concepts = [(c, _evidence(origin_articles, c)) for c in _concepts(origin, origin_articles)]
    concepts = [(c, evidence) for c, evidence in concepts if evidence]
    candidates = db.query('SELECT * FROM stories WHERE id != ? ORDER BY created_at DESC, id LIMIT ?', (story_id, MAX_CANDIDATES))
    ranked = []
    for candidate in candidates:
        fields = json.loads(candidate['subfields'])
        if candidate['lang'] not in profile['languages'] or (fields and max(fields, key=fields.get) in profile['excluded_subfields']):
            continue
        ids = set(json.loads(candidate['article_ids']))
        other_articles = articles(candidate)
        urls = {a['url'] for a in other_articles}
        if ids & origin_ids or urls & origin_urls:
            continue
        matches = []
        for concept, left in concepts:
            right = _evidence(other_articles, concept)
            if not right:
                continue
            # A body-only mention can be incidental or scraped page boilerplate.
            # Both headlines must name the concept AND share independent context.
            left_title = _evidence(origin_articles, concept, title_only=True)
            right_title = _evidence(other_articles, concept, title_only=True)
            if not left_title or not right_title:
                continue
            shared = (_terms(left_title['text']) & _terms(right_title['text'])) - _terms(concept)
            if len(shared) < 2:
                continue
            score = (len(shared), len(_terms(concept)))
            matches.append((score, concept, left_title, right_title))
        if matches:
            score, concept, left, right = max(matches, key=lambda m: m[0])
            ranked.append((score, candidate['id'], ids, urls,
                           {'story_id': candidate['id'], 'title': right['title'],
                            'concept': concept, 'evidence': [left, right]}))
    # Rank the whole bounded pool before limiting; recency is not relevance.
    ranked.sort(key=lambda item: (item[0], item[1]), reverse=True)
    links, seen_ids, seen_urls = [], set(origin_ids), set(origin_urls)
    for _, _, ids, urls, link in ranked:
        if ids & seen_ids or urls & seen_urls:
            continue
        links.append(link)
        seen_ids.update(ids)
        seen_urls.update(urls)
        if len(links) == MAX_CONNECTIONS:
            break
    return {'connections': links, 'candidate_limit': MAX_CANDIDATES, 'limit': MAX_CONNECTIONS}
