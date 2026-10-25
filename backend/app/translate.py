"""Translate generated payloads into Malayalam (cached). Only string leaves under selected keys are translated."""

import json

from . import db, llm
from .config import FAST_MODEL

LANG_NAMES = {"ml": "Malayalam"}
TRANSLATABLE = {"quick", "standard", "deep", "text", "question", "why", "blurb", "heading", "event", "title"}

SYSTEM = """Translate each string in the JSON array into natural, clear {lang} as used by a quality newspaper.
Keep names, numbers and citation refs unchanged. Return {{"t": [translated strings in the same order]}}."""


def _collect(obj, out, key=None):
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k in ("sources", "articles", "search", "concepts", "url"):
                continue
            _collect(v, out, k)
    elif isinstance(obj, list):
        for v in obj:
            _collect(v, out, key)
    elif isinstance(obj, str) and key in TRANSLATABLE and obj.strip():
        out.append(obj)


def _apply(obj, mapping, key=None):
    if isinstance(obj, dict):
        return {k: (v if k in ("sources", "articles", "search", "concepts", "url") else _apply(v, mapping, k)) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_apply(v, mapping, key) for v in obj]
    if isinstance(obj, str) and key in TRANSLATABLE:
        return mapping.get(obj, obj)
    return obj


def translate_payload(payload, lang):
    if lang not in LANG_NAMES:
        return payload
    strings = []
    _collect(payload, strings)
    strings = list(dict.fromkeys(strings))
    if not strings:
        return payload
    data = llm.chat_json(SYSTEM.format(lang=LANG_NAMES[lang]), json.dumps(strings, ensure_ascii=False), model=FAST_MODEL, max_output_tokens=12000)
    if not isinstance(data, dict) or not isinstance(data.get("t"), list) or len(data["t"]) != len(strings) or any(not isinstance(t, str) or not t.strip() for t in data["t"]):
        return {**payload, "translation": "unavailable"}
    return {**_apply(payload, dict(zip(strings, data["t"]))), "translation": lang}


def translated_analysis(story_id, analysis, lang):
    rows = db.query("SELECT translations FROM stories WHERE id=?", (story_id,))
    cache = json.loads(rows[0]["translations"] or "{}") if rows else {}
    if lang in cache and cache[lang].get("version") == analysis.get("version") and cache[lang].get("mode") == analysis.get("mode"):
        return cache[lang]
    out = translate_payload(analysis, lang)
    if out.get("translation") == lang:
        cache[lang] = out
        with db.tx() as c:
            c.execute("UPDATE stories SET translations=? WHERE id=?", (json.dumps(cache, ensure_ascii=False), story_id))
    return out
