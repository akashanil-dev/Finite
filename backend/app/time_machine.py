"""A finite, source-extractive timeline. No network requests or AI generation."""
import calendar
import json
import math
import re
from datetime import datetime, timezone

from . import db
from .sources import SOURCE_MAP
from .textutil import SENT_RE

MONTHS = {name.lower(): i for i, name in enumerate(calendar.month_name) if name}
MONTH = '|'.join(MONTHS)
DATE = re.compile(rf'\b(?:\d{{4}}-\d{{2}}-\d{{2}}|(?:{MONTH})\s+\d{{1,2}}(?:st|nd|rd|th)?(?:,?\s+\d{{4}})?|\d{{1,2}}(?:st|nd|rd|th)?\s+(?:{MONTH})(?:\s+\d{{4}})?|(?:1[5-9]|20)\d{{2}})\b', re.I)
MAX_EVENTS = 12


def date_info(text):
    """Never infer a missing year or select one date from an ambiguous sentence."""
    matches = list(dict.fromkeys(m.group() for m in DATE.finditer(text)))
    if not matches:
        return None
    if len(matches) != 1:
        return {'date': ' / '.join(matches), 'sort_date': None, 'precision': 'multiple_dates'}
    label = matches[0]
    if re.fullmatch(r'\d{4}', label):
        return {'date': label, 'sort_date': label + '-01-01', 'precision': 'year'}
    normalized = re.sub(r'(\d)(st|nd|rd|th)\b', r'\1', label, flags=re.I).replace(',', '')
    for fmt in ('%Y-%m-%d', '%B %d %Y', '%d %B %Y'):
        try:
            value = datetime.strptime(normalized, fmt)
            return {'date': label, 'sort_date': value.strftime('%Y-%m-%d'), 'precision': 'day'}
        except ValueError:
            pass
    return {'date': label, 'sort_date': None, 'precision': 'unresolved'}


def _timestamp(value):
    if not isinstance(value, (int, float)) or not math.isfinite(value) or value <= 0:
        return None
    try:
        return datetime.fromtimestamp(value, timezone.utc).isoformat()
    except (ValueError, OverflowError, OSError):
        return None


def timeline(story_id):
    rows = db.query('SELECT article_ids FROM stories WHERE id=?', (story_id,))
    if not rows:
        return None
    ids = json.loads(rows[0]['article_ids'])
    articles = db.query(f"SELECT * FROM articles WHERE id IN ({','.join('?' for _ in ids)})", ids) if ids else []
    articles.sort(key=lambda a: (a.get('published_at') or 0, a['id']))
    publication_dates = [v for a in articles if (v := _timestamp(a.get('published_at')))]
    coverage_year = min(publication_dates)[:4] if publication_dates else None
    sources, coverage, events = {}, [], {}
    for i, article in enumerate(articles):
        ref = f'T{i + 1}'
        src = SOURCE_MAP.get(article['source_id'], {})
        sources[ref] = {'name': src.get('name', article['source_id']), 'title': article['title'],
                        'url': article['url'], 'weight': src.get('weight', 0.5), 'kind': 'news'}
        published = _timestamp(article.get('published_at'))
        updated = _timestamp(article.get('updated_at'))
        coverage.append({'title': article['title'], 'published_at': published,
                         'updated_at': updated if updated and published and updated > published else None,
                         'citations': [ref]})
        for sentence in SENT_RE.split(article.get('content') or article.get('description') or ''):
            sentence = sentence.strip()
            # Short, complete quotations; never truncate away qualifying context.
            if not 20 <= len(sentence) <= 600:
                continue
            date = date_info(sentence)
            if not date:
                continue
            key = re.sub(r'\s+', ' ', sentence).casefold()
            if key in events:
                events[key]['citations'].append(ref)
                continue
            group = 'unresolved'
            if date['sort_date']:
                group = 'background' if coverage_year and date['sort_date'][:4] < coverage_year else 'current'
            events[key] = {**date, 'text': sentence, 'citations': [ref], 'group': group}
    ordered = sorted(events.values(), key=lambda e: (e['sort_date'] is None, e['sort_date'] or '', e['text']))
    return {'mode': 'extractive', 'events': ordered[:MAX_EVENTS], 'total_events': len(ordered),
            'coverage': coverage, 'sources': sources, 'coverage_year': coverage_year,
            'status': 'available' if ordered else 'no_dated_events'}
