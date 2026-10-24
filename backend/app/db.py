import json
import sqlite3
import threading
from contextlib import contextmanager

from .config import DB_PATH

_lock = threading.Lock()

SCHEMA = """
CREATE TABLE IF NOT EXISTS articles (
    id TEXT PRIMARY KEY,
    source_id TEXT NOT NULL,
    lang TEXT NOT NULL,
    title TEXT NOT NULL,
    url TEXT NOT NULL,
    description TEXT,
    content TEXT,
    published_at REAL,
    updated_at REAL,
    fetched_at REAL NOT NULL,
    subfields TEXT DEFAULT '{}',
    story_type TEXT,
    classified INTEGER DEFAULT 0
);
CREATE INDEX IF NOT EXISTS idx_articles_pub ON articles(published_at);

CREATE TABLE IF NOT EXISTS stories (
    id TEXT PRIMARY KEY,
    article_ids TEXT NOT NULL,
    title TEXT NOT NULL,
    lang TEXT NOT NULL,
    subfields TEXT NOT NULL,
    story_type TEXT,
    created_at REAL NOT NULL,
    analysis TEXT,
    translations TEXT DEFAULT '{}'
);

CREATE TABLE IF NOT EXISTS briefings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created_at REAL NOT NULL,
    window_start REAL NOT NULL,
    window_end REAL NOT NULL,
    config TEXT NOT NULL,
    story_ids TEXT NOT NULL,
    read_ids TEXT DEFAULT '[]',
    completed_at REAL
);

CREATE TABLE IF NOT EXISTS explorations (
    key TEXT PRIMARY KEY,
    story_id TEXT NOT NULL,
    payload TEXT NOT NULL,
    created_at REAL NOT NULL
);

CREATE TABLE IF NOT EXISTS journeys (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    story_id TEXT NOT NULL,
    story_title TEXT NOT NULL,
    path TEXT NOT NULL,
    concepts TEXT NOT NULL,
    created_at REAL NOT NULL
);

CREATE TABLE IF NOT EXISTS kv (
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL
);
"""


def connect():
    conn = sqlite3.connect(DB_PATH, timeout=30, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    return conn


@contextmanager
def tx():
    with _lock:
        conn = connect()
        try:
            yield conn
            conn.commit()
        finally:
            conn.close()


def query(sql, params=()):
    conn = connect()
    try:
        return [dict(r) for r in conn.execute(sql, params).fetchall()]
    finally:
        conn.close()


def init():
    with tx() as c:
        c.executescript(SCHEMA)


def kv_get(key, default=None):
    rows = query("SELECT value FROM kv WHERE key=?", (key,))
    return json.loads(rows[0]["value"]) if rows else default


def kv_set(key, value):
    with tx() as c:
        c.execute("INSERT INTO kv(key,value) VALUES(?,?) ON CONFLICT(key) DO UPDATE SET value=excluded.value", (key, json.dumps(value)))
