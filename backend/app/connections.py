"""Finite cross-story comparisons using literal source evidence, never generated links."""
import json
import re

from . import briefing, db
from .sources import SOURCE_MAP
from .textutil import SENT_RE

MAX_CONNECTIONS = 3
MAX_CANDIDATES = 200
# Extractive concepts sometimes contain sentence starters or generic roles.
GENERIC = {'after', 'before', 'during', 'according', 'considering', 'story', 'union',
           'police', 'protesters', 'chief minister', 'government', 'india', 'news'}


def _concepts(story):
    analysis = json.loads(story['analysis'] or '{}')
    values = analysis.get('concepts', [])
    if not isinstance(values, list):
        return []
    return list(dict.fromkeys(v.strip() for v in values if isinstance(v, str)
                             and 3 <= len(v.strip()) <= 80 and v.strip().casefold() not in GENERIC))[:30]


def _evidence(articles, concept):
    pattern = re.compile(r'(?<!\w)' + re.escape(concept) + r'(?!\w)', re.IGNORECASE)
    for article in articles:
        passages = [article['title'], *SENT_RE.split(article.get('content') or article.get('description') or '')]
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
    concepts = [(c, _evidence(origin_articles, c)) for c in _concepts(origin)]
    concepts = [(c, evidence) for c, evidence in concepts if evidence]
    candidates = db.query('SELECT * FROM stories WHERE id != ? ORDER BY created_at DESC, id LIMIT ?', (story_id, MAX_CANDIDATES))
    links, seen_ids, seen_urls = [], set(origin_ids), set(origin_urls)
    for candidate in candidates:
        fields = json.loads(candidate['subfields'])
        if candidate['lang'] not in profile['languages'] or (fields and max(fields, key=fields.get) in profile['excluded_subfields']):
            continue
        ids = set(json.loads(candidate['article_ids']))
        other_articles = articles(candidate)
        urls = {a['url'] for a in other_articles}
        if ids & seen_ids or urls & seen_urls:
            continue
        matches = [(c, left, _evidence(other_articles, c)) for c, left in concepts]
        matches = [(c, left, right) for c, left, right in matches if right]
        if not matches:
            continue
        # Prefer a specific phrase over a short single-word match.
        concept, left, right = max(matches, key=lambda m: (len(m[0].split()), len(m[0])))
        links.append({'story_id': candidate['id'], 'title': right['title'], 'concept': concept,
                      'evidence': [left, right]})
        seen_ids.update(ids)
        seen_urls.update(urls)
        if len(links) == MAX_CONNECTIONS:
            break
    return {'connections': links, 'candidate_limit': MAX_CANDIDATES, 'limit': MAX_CONNECTIONS}
