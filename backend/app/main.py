import concurrent.futures as cf
import json
import logging
import threading
import time
from collections import Counter
from contextlib import asynccontextmanager
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from . import analysis, briefing, budget, db, ingest, perspectives, rabbithole, translate
from .config import APP_NAME, FAST_MODEL, INGEST_INTERVAL_MIN, MAX_DEPTH, MOCK_MODE, PREPARE_BEFORE_MIN, SMART_MODEL
from .sources import public_sources
from .taxonomy import SUBFIELDS, public_taxonomy

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(name)s %(levelname)s %(message)s")
log = logging.getLogger("finite")
pool = cf.ThreadPoolExecutor(4)
_ingest_lock = threading.Lock()


def do_ingest():
    if not _ingest_lock.acquire(blocking=False):
        return db.kv_get("last_ingest")
    try:
        return ingest.run_ingest()
    finally:
        _ingest_lock.release()


def prefetch(bid):
    payload = briefing.briefing_payload(bid)
    for s in (payload or {}).get("stories", []):
        pool.submit(analysis.analyze, s["id"])


def make_briefing():
    bid = briefing.build_briefing()
    if bid:
        prefetch(bid)
    return bid


def scheduler():
    """Ingest periodically; freeze a briefing PREPARE_BEFORE_MIN before the user's delivery time."""
    while True:
        try:
            last = db.kv_get("last_ingest") or {}
            if time.time() - last.get("at", 0) > INGEST_INTERVAL_MIN * 60:
                do_ingest()
            p = briefing.get_profile()
            if p["onboarded"]:
                tz = ZoneInfo(p["timezone"])
                now = datetime.now(tz)
                hh, mm = map(int, p["delivery_time"].split(":"))
                prepare_at = now.replace(hour=hh, minute=mm, second=0, microsecond=0) - timedelta(minutes=PREPARE_BEFORE_MIN)
                latest = db.query("SELECT created_at FROM briefings ORDER BY id DESC LIMIT 1")
                if now >= prepare_at and (not latest or latest[0]["created_at"] < prepare_at.timestamp()):
                    do_ingest()
                    make_briefing()
        except Exception:
            log.exception("scheduler tick failed")
        time.sleep(300)


@asynccontextmanager
async def lifespan(app):
    db.init()
    threading.Thread(target=scheduler, daemon=True).start()
    yield


app = FastAPI(title=f"{APP_NAME} API", lifespan=lifespan)
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])


@app.get("/api/meta")
def meta():
    return {"app_name": APP_NAME, "mock_mode": MOCK_MODE, "models": {"fast": FAST_MODEL, "smart": SMART_MODEL}, "max_depth": MAX_DEPTH,
            "taxonomy": public_taxonomy(), "last_ingest": db.kv_get("last_ingest"),
            "languages": [{"id": "en", "name": "English"}, {"id": "ml", "name": "Malayalam", "native": "മലയാളം"}],
            "periods": [{"id": "morning", "label": "Morning", "range": "7–9 AM", "time": "07:30"}, {"id": "noon", "label": "Noon", "range": "12–2 PM", "time": "12:30"},
                        {"id": "evening", "label": "Evening", "range": "5–7 PM", "time": "17:30"}, {"id": "night", "label": "Night", "range": "9–11 PM", "time": "21:30"}],
            "depths": [{"id": "quick", "label": "Quick", "desc": "30-second summaries"}, {"id": "standard", "label": "Standard", "desc": "2-minute explanations"},
                       {"id": "deep", "label": "Deep", "desc": "5-minute analysis"}]}


@app.get("/api/ai-budget")
def ai_budget():
    return budget.status()


@app.get("/api/sources")
def sources():
    return public_sources()


@app.get("/api/profile")
def get_profile():
    return briefing.get_profile()


@app.put("/api/profile")
def put_profile(p: dict):
    return briefing.save_profile(p)


@app.post("/api/ingest")
def run_ingest():
    return do_ingest()


@app.post("/api/briefings")
def create_briefing(refresh: bool = True):
    if refresh:
        do_ingest()
    bid = make_briefing()
    if not bid:
        raise HTTPException(404, "No stories matched your interests in this window. Try adding interests or widening the lookback.")
    return briefing.briefing_payload(bid)


@app.get("/api/briefings/latest")
def latest_briefing():
    rows = db.query("SELECT id FROM briefings ORDER BY id DESC LIMIT 1")
    return briefing.briefing_payload(rows[0]["id"]) if rows else None


@app.get("/api/briefings/{bid}")
def get_briefing(bid: int):
    out = briefing.briefing_payload(bid)
    if not out:
        raise HTTPException(404)
    return out


class ReadBody(BaseModel):
    story_id: str


@app.post("/api/briefings/{bid}/read")
def read_story(bid: int, body: ReadBody):
    out = briefing.mark_read(bid, body.story_id)
    if not out:
        raise HTTPException(404)
    return out


@app.get("/api/stories/{story_id}")
def get_story(story_id: str, lang: str = "en"):
    rows = db.query("SELECT * FROM stories WHERE id=?", (story_id,))
    if not rows:
        raise HTTPException(404, "Story not found")
    a = analysis.analyze(story_id)
    if lang != "en":
        a = translate.translated_analysis(story_id, a, lang)
    return {"card": briefing.story_card(db.query("SELECT * FROM stories WHERE id=?", (story_id,))[0]), "analysis": a}


@app.get("/api/stories/{story_id}/perspectives")
def story_perspectives(story_id: str):
    out = perspectives.compare(story_id)
    if out is None:
        raise HTTPException(404, "Story not found")
    return out


class ExploreBody(BaseModel):
    question: str
    angle: str = "context"
    search: list[str] = []
    depth: int = 1
    custom: bool = False
    path: list[dict] = []
    lang: str = "en"


@app.post("/api/stories/{story_id}/explore")
def explore(story_id: str, body: ExploreBody):
    q = body.question.strip()[:300]
    if not q:
        raise HTTPException(400, "Empty question")
    out = rabbithole.explore(story_id, q, body.angle, body.search, body.depth, body.custom, body.path)
    if out is None:
        raise HTTPException(404, "Story not found")
    if body.lang != "en" and not out.get("off_topic"):
        out = translate.translate_payload(out, body.lang)
    return out


class JourneyBody(BaseModel):
    story_id: str
    path: list[dict]
    concepts: list[str] = []


@app.post("/api/journeys")
def save_journey(body: JourneyBody):
    s = db.query("SELECT title, subfields FROM stories WHERE id=?", (body.story_id,))
    if not s:
        raise HTTPException(404)
    with db.tx() as c:
        c.execute("INSERT INTO journeys(story_id, story_title, path, concepts, created_at) VALUES(?,?,?,?,?)",
                  (body.story_id, s[0]["title"], json.dumps(body.path), json.dumps(list(dict.fromkeys(body.concepts))), time.time()))
    return passport()


@app.get("/api/passport")
def passport():
    journeys = db.query("SELECT j.*, s.subfields FROM journeys j JOIN stories s ON s.id=j.story_id ORDER BY j.created_at DESC")
    concepts, areas = Counter(), Counter()
    for j in journeys:
        j["path"], j["concepts"] = json.loads(j["path"]), json.loads(j["concepts"])
        concepts.update(j["concepts"])
        for sid in json.loads(j.pop("subfields")):
            if sid in SUBFIELDS:
                areas[SUBFIELDS[sid]["name"]] += 1
    briefings_done = db.query("SELECT COUNT(*) n FROM briefings WHERE completed_at IS NOT NULL")[0]["n"]
    return {"journeys": journeys, "concepts": [{"name": k, "count": v} for k, v in concepts.most_common()],
            "areas": [{"name": k, "count": v} for k, v in areas.most_common()], "briefings_completed": briefings_done,
            "questions_explored": sum(len(j["path"]) for j in journeys)}
