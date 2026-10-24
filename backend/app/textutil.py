import hashlib
import re
from html import unescape

ML_RE = re.compile(r"[\u0D00-\u0D7F]")
OTHER_INDIC_RE = re.compile(r"[\u0900-\u0CFF\u0D80-\u0DFF]")
TAG_RE = re.compile(r"<[^>]+>")
WS_RE = re.compile(r"\s+")
SENT_RE = re.compile(r"(?<=[.!?।])\s+(?=[A-Z\u0D00-\u0D7F\"'‘“(])")


def hid(*parts) -> str:
    return hashlib.sha1("|".join(parts).encode()).hexdigest()[:16]


def clean_html(s: str | None) -> str:
    return WS_RE.sub(" ", unescape(TAG_RE.sub(" ", s or ""))).strip()


def detect_lang(text: str) -> str:
    ml = len(ML_RE.findall(text))
    other = len(OTHER_INDIC_RE.findall(text))
    if ml > 5 and ml >= other:
        return "ml"
    if other > 5:
        return "other"
    return "en"


def sentences(text: str) -> list[str]:
    return [s.strip() for s in SENT_RE.split(text or "") if len(s.strip()) > 30]


def words(text: str) -> set[str]:
    return set(re.findall(r"[a-z0-9][a-z0-9\-()]+", (text or "").lower()))


def chunk(text: str, size: int = 700) -> list[str]:
    """Split text into ~size-char passages on sentence boundaries."""
    out, cur = [], ""
    for s in sentences(text) or [text]:
        if len(cur) + len(s) > size and cur:
            out.append(cur.strip())
            cur = ""
        cur += " " + s
    if cur.strip():
        out.append(cur.strip())
    return out
