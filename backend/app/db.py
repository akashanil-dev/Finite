import json
import sqlite3
import threading
from contextlib import contextmanager

from .config import DB_PATH

_lock = threading.Lock()

SCHEMA = """
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    is_admin INTEGER NOT NULL DEFAULT 0,
    created_at REAL NOT NULL
);
CREATE TABLE IF NOT EXISTS sessions (
    token_hash TEXT PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id),
    expires_at REAL NOT NULL
);
CREATE INDEX IF NOT EXISTS sessions_user ON sessions(user_id);
CREATE TABLE IF NOT EXISTS auth_attempts (
    key TEXT PRIMARY KEY,
    started_at REAL NOT NULL,
    attempts INTEGER NOT NULL
);
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
        if 'is_admin' not in {row['name'] for row in c.execute('PRAGMA table_info(users)')}:
            c.execute('ALTER TABLE users ADD COLUMN is_admin INTEGER NOT NULL DEFAULT 0')
        briefing_columns = {row['name'] for row in c.execute('PRAGMA table_info(briefings)')}
        for name, definition in [('refresh_used', 'INTEGER NOT NULL DEFAULT 0'), ('edition_of', 'INTEGER'), ('scheduled_for', 'TEXT'), ('opened_at', 'REAL')]:
            if name not in briefing_columns:
                c.execute(f'ALTER TABLE briefings ADD COLUMN {name} {definition}')
        c.execute('CREATE TABLE IF NOT EXISTS briefing_requests (request_key TEXT PRIMARY KEY, created_at REAL NOT NULL)')
        # Additive migration: legacy local data stays unassigned until explicitly claimed.
        for table in ('briefings', 'journeys'):
            columns = {row['name'] for row in c.execute(f'PRAGMA table_info({table})')}
            if 'user_id' not in columns:
                c.execute(f'ALTER TABLE {table} ADD COLUMN user_id INTEGER REFERENCES users(id)')
            c.execute(f'CREATE INDEX IF NOT EXISTS {table}_user ON {table}(user_id)')
        c.execute('CREATE UNIQUE INDEX IF NOT EXISTS briefing_schedule ON briefings(user_id,scheduled_for) WHERE scheduled_for IS NOT NULL')


def kv_get(key, default=None):
    rows = query("SELECT value FROM kv WHERE key=?", (key,))
    return json.loads(rows[0]["value"]) if rows else default


def kv_set(key, value):
    with tx() as c:
        c.execute("INSERT INTO kv(key,value) VALUES(?,?) ON CONFLICT(key) DO UPDATE SET value=excluded.value", (key, json.dumps(value)))
