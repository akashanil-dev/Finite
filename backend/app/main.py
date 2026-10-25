import concurrent.futures as cf
import json
import os
import logging
import threading
import time
from collections import Counter
from contextlib import asynccontextmanager
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, field_validator

from . import analysis, auth, briefing, budget, connections, db, ingest, perspectives, rabbithole, time_machine, translate
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


def prefetch(bid, user_id):
    payload = briefing.briefing_payload(bid, user_id)
    for s in (payload or {}).get("stories", []):
        pool.submit(analysis.analyze, s["id"])


def make_briefing(user_id, **options):
    bid = briefing.build_briefing(user_id=user_id, **options)
    if bid:
        prefetch(bid, user_id)
    return bid


def due_schedule(profile, now=None):
    now = now or datetime.now(ZoneInfo(profile['timezone']))
    hh, mm = map(int, profile['delivery_time'].split(':'))
    delivery = now.replace(hour=hh, minute=mm, second=0, microsecond=0)
    lead = timedelta(minutes=PREPARE_BEFORE_MIN)
    # A just-after-midnight delivery must be prepared on the previous evening.
    if now >= delivery + timedelta(days=1) - lead:
        delivery += timedelta(days=1)
    return delivery.date().isoformat() if now >= delivery - lead else None


def scheduler():
    """Ingest periodically; freeze a briefing PREPARE_BEFORE_MIN before the user's delivery time."""
    while True:
        try:
            last = db.kv_get("last_ingest") or {}
            if time.time() - last.get("at", 0) > INGEST_INTERVAL_MIN * 60:
                do_ingest()
            for account in db.query("SELECT id FROM users"):
                user_id = account['id']
                p = briefing.get_profile(user_id)
                if p["onboarded"]:
                    schedule_key = due_schedule(p)
                    latest = db.query("SELECT id FROM briefings WHERE user_id=? AND scheduled_for=?", (user_id, schedule_key))
                    if schedule_key and not latest:
                        make_briefing(user_id, scheduled_for=schedule_key)
        except Exception:
            log.exception("scheduler tick failed")
        time.sleep(300)


@asynccontextmanager
async def lifespan(app):
    db.init()
    if os.getenv("FINITE_SCHEDULER_ENABLED", "true").lower() == "true":
        threading.Thread(target=scheduler, daemon=True).start()
    yield


app = FastAPI(title=f"{APP_NAME} API", lifespan=lifespan, dependencies=[Depends(auth.require_user)])
app.add_middleware(CORSMiddleware, allow_origins=auth.ORIGINS, allow_credentials=True,
                   allow_methods=["GET", "POST", "PUT"], allow_headers=["Content-Type", "X-Finite-Request"])
app.include_router(auth.router)


@app.middleware("http")
async def protect_browser_requests(request: Request, call_next):
    from fastapi.responses import JSONResponse
    if request.url.path.startswith('/api/') and request.method not in {'GET', 'HEAD', 'OPTIONS'}:
        origin = request.headers.get('origin')
        if request.headers.get('x-finite-request') != '1' or (origin and origin not in auth.ORIGINS):
            return JSONResponse({'detail': 'Request origin not allowed'}, status_code=403)
    response = await call_next(request)
    if request.url.path.startswith('/api/'):
        response.headers['Cache-Control'] = 'no-store'
    return response


@app.get('/api/health')
def health():
    db.query('SELECT 1')
    return {'status': 'ok'}


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
def ai_budget(user=Depends(auth.require_admin)):
    return budget.status()


@app.get("/api/sources")
def sources():
    return public_sources()


@app.get("/api/profile")
def get_profile(user=Depends(auth.require_user)):
    return briefing.get_profile(user["id"])


class ProfileBody(BaseModel):
    onboarded: bool = False
    languages: list[str] = Field(default_factory=lambda: ['en'], max_length=2)
    ui_language: str = 'en'
    interests: dict[str, int] = Field(default_factory=dict, max_length=200)
    excluded_subfields: list[str] = Field(default_factory=list, max_length=200)
    excluded_sources: list[str] = Field(default_factory=list, max_length=200)
    delivery_time: str = Field(default='07:30', pattern=r'^([01][0-9]|2[0-3]):[0-5][0-9]$')
    timezone: str = 'Asia/Kolkata'
    lookback_hours: int = Field(default=30, ge=6, le=72)
    stories_per_briefing: int = Field(default=12, ge=3, le=25)
    depth: str = 'standard'

    @field_validator('timezone')
    @classmethod
    def valid_timezone(cls, value):
        try:
            ZoneInfo(value)
        except (KeyError, ValueError):
            raise ValueError('Choose a valid timezone') from None
        return value

    @field_validator('ui_language')
    @classmethod
    def valid_language(cls, value):
        if value not in {'en', 'ml'}:
            raise ValueError('Unsupported language')
        return value

    @field_validator('languages')
    @classmethod
    def valid_languages(cls, value):
        if any(v not in {'en', 'ml'} for v in value):
            raise ValueError('Unsupported language')
        return value

    @field_validator('depth')
    @classmethod
    def valid_depth(cls, value):
        if value not in {'quick', 'standard', 'deep'}:
            raise ValueError('Unsupported depth')
        return value


@app.put("/api/profile")
def put_profile(p: ProfileBody, user=Depends(auth.require_user)):
    return briefing.save_profile(p.model_dump(), user['id'])


@app.post("/api/ingest")
def run_ingest(user=Depends(auth.require_admin)):
    return do_ingest()


@app.get("/api/briefings")
def briefing_history(before: int | None = None, user=Depends(auth.require_user)):
    return briefing.list_briefings(user['id'], before)


@app.post("/api/briefings")
def create_briefing(refresh: bool = True, user=Depends(auth.require_user)):
    # Claim before ingestion: concurrent clicks cannot spend repeatedly or create duplicates.
    key = f"first-briefing:{user['id']}"
    with db.tx() as c:
        c.execute('BEGIN IMMEDIATE')
        if c.execute('SELECT id FROM briefings WHERE user_id=? LIMIT 1', (user['id'],)).fetchone():
            raise HTTPException(409, "Your briefings are saved. Use an edition's one-time New edition action.")
        if not c.execute('INSERT OR IGNORE INTO briefing_requests VALUES(?,?)', (key,time.time())).rowcount:
            raise HTTPException(409, "Your first briefing is already being prepared.")
    try:
        if refresh:
            do_ingest()
        bid = make_briefing(user['id'])
        if not bid:
            raise HTTPException(404, "No new stories matched your interests. Your saved editions are unchanged.")
        return briefing.briefing_payload(bid, user['id'])
    finally:
        with db.tx() as c:
            c.execute('DELETE FROM briefing_requests WHERE request_key=?', (key,))


@app.post("/api/briefings/{bid}/edition")
def extra_edition(bid: int, user=Depends(auth.require_user)):
    with db.tx() as c:
        c.execute('BEGIN IMMEDIATE')
        row = c.execute('SELECT * FROM briefings WHERE id=? AND user_id=?', (bid,user['id'])).fetchone()
        if not row:
            raise HTTPException(404, "Briefing not found")
        if row['refresh_used'] or row['edition_of'] is not None:
            raise HTTPException(409, "This edition has already used its one-time refresh.")
        c.execute('UPDATE briefings SET refresh_used=1 WHERE id=?', (bid,))
    do_ingest()
    new_id = make_briefing(user['id'], edition_of=bid)
    if not new_id:
        raise HTTPException(404, "No new matching stories were available. This edition's refresh has been used; all saved briefs remain available.")
    return briefing.briefing_payload(new_id, user['id'])


@app.get("/api/briefings/latest")
def latest_briefing(user=Depends(auth.require_user)):
    rows = db.query("SELECT id FROM briefings WHERE user_id=? ORDER BY id DESC LIMIT 1", (user["id"],))
    return briefing.briefing_payload(rows[0]["id"], user["id"]) if rows else None


@app.get("/api/briefings/{bid}")
def get_briefing(bid: int, user=Depends(auth.require_user)):
    out = briefing.briefing_payload(bid, user["id"])
    if not out:
        raise HTTPException(404)
    return out


class ReadBody(BaseModel):
    story_id: str


@app.post("/api/briefings/{bid}/read")
def read_story(bid: int, body: ReadBody, user=Depends(auth.require_user)):
    out = briefing.mark_read(bid, body.story_id, user["id"])
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


@app.get("/api/stories/{story_id}/timeline")
def story_timeline(story_id: str):
    out = time_machine.timeline(story_id)
    if out is None:
        raise HTTPException(404, "Story not found")
    return out


@app.get("/api/stories/{story_id}/connections")
def story_connections(story_id: str, user=Depends(auth.require_user)):
    out = connections.explore(story_id, user["id"])
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
def save_journey(body: JourneyBody, user=Depends(auth.require_user)):
    s = db.query("SELECT title, subfields FROM stories WHERE id=?", (body.story_id,))
    if not s:
        raise HTTPException(404)
    with db.tx() as c:
        c.execute("INSERT INTO journeys(story_id, story_title, path, concepts, created_at, user_id) VALUES(?,?,?,?,?,?)",
                  (body.story_id, s[0]["title"], json.dumps(body.path), json.dumps(list(dict.fromkeys(body.concepts))), time.time(), user["id"]))
    return passport(user)


@app.get("/api/passport")
def passport(user=Depends(auth.require_user)):
    journeys = db.query("SELECT j.*, s.subfields FROM journeys j JOIN stories s ON s.id=j.story_id WHERE j.user_id=? ORDER BY j.created_at DESC", (user["id"],))
    concepts, areas = Counter(), Counter()
    for j in journeys:
        j["path"], j["concepts"] = json.loads(j["path"]), json.loads(j["concepts"])
        concepts.update(j["concepts"])
        for sid in json.loads(j.pop("subfields")):
            if sid in SUBFIELDS:
                areas[SUBFIELDS[sid]["name"]] += 1
    briefings_done = db.query("SELECT COUNT(*) n FROM briefings WHERE completed_at IS NOT NULL AND user_id=?", (user["id"],))[0]["n"]
    return {"journeys": journeys, "concepts": [{"name": k, "count": v} for k, v in concepts.most_common()],
            "areas": [{"name": k, "count": v} for k, v in areas.most_common()], "briefings_completed": briefings_done,
            "questions_explored": sum(len(j["path"]) for j in journeys)}
