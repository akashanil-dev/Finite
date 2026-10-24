"""OpenAI wrapper with on-disk caching. Returns None in mock mode so callers fall back to extractive logic."""

import hashlib
import json
import logging

from .config import EMBED_MODEL, FAST_MODEL, LLM_CACHE_DIR, MOCK_MODE, OPENAI_API_KEY

log = logging.getLogger("finite.llm")
_client = None


def _get_client():
    global _client
    if _client is None:
        from openai import OpenAI
        _client = OpenAI(api_key=OPENAI_API_KEY)
    return _client


def _cache_path(kind, payload):
    h = hashlib.sha256(json.dumps(payload, sort_keys=True, ensure_ascii=False).encode()).hexdigest()[:32]
    return LLM_CACHE_DIR / f"{kind}-{h}.json"


def chat_json(system: str, user: str, model: str = FAST_MODEL, max_output_tokens: int = 4000):
    """Ask the model for a JSON object. Returns dict, or None if unavailable."""
    if MOCK_MODE:
        return None
    path = _cache_path("chat", {"s": system, "u": user, "m": model})
    if path.exists():
        return json.loads(path.read_text())
    try:
        resp = _get_client().responses.create(
            model=model,
            instructions=system + "\n\nRespond with a single valid JSON object only.",
            input=user,
            text={"format": {"type": "json_object"}},
            max_output_tokens=max_output_tokens,
        )
        data = json.loads(resp.output_text)
    except Exception as e:  # network, quota, malformed JSON: degrade gracefully
        log.warning("LLM call failed (%s): %s", model, e)
        return None
    path.write_text(json.dumps(data, ensure_ascii=False))
    return data


def embed(texts: list[str]):
    """Return list of embedding vectors, or None in mock mode / on failure."""
    if MOCK_MODE or not texts:
        return None
    path = _cache_path("embed", {"t": texts, "m": EMBED_MODEL})
    if path.exists():
        return json.loads(path.read_text())
    try:
        out = []
        for i in range(0, len(texts), 256):
            resp = _get_client().embeddings.create(model=EMBED_MODEL, input=[t[:2000] for t in texts[i:i + 256]])
            out.extend(d.embedding for d in resp.data)
    except Exception as e:
        log.warning("Embedding call failed: %s", e)
        return None
    path.write_text(json.dumps(out))
    return out
