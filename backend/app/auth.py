"""Username/password accounts and revocable, opaque cookie sessions."""
import hashlib
import hmac
import os
import re
import secrets
import sqlite3
import time

from fastapi import APIRouter, Depends, HTTPException, Request, Response
from pydantic import BaseModel, Field

from . import db

COOKIE = 'finite_session'
SESSION_SECONDS = 30 * 24 * 3600
SECURE_COOKIE = os.getenv('FINITE_SECURE_COOKIES', 'false').lower() == 'true'
ORIGINS = [v.strip() for v in os.getenv('FINITE_ALLOWED_ORIGINS', 'http://localhost:3000,http://127.0.0.1:3000').split(',') if v.strip()]
PUBLIC_PATHS = {'/api/health', '/api/auth/register', '/api/auth/login'}
router = APIRouter(prefix='/api/auth')


def digest(token):
    return hashlib.sha256(token.encode()).hexdigest()


def hash_password(password, salt=None):
    salt = salt or secrets.token_hex(16)
    value = hashlib.scrypt(password.encode(), salt=bytes.fromhex(salt), n=32768, r=8, p=3, maxmem=64 * 1024 * 1024).hex()
    return f'scrypt${salt}${value}'


DUMMY_HASH = hash_password('unused-password-for-timing')


def verify_password(password, stored):
    try:
        _, salt, _ = stored.split('$')
        return hmac.compare_digest(hash_password(password, salt), stored)
    except (ValueError, TypeError):
        return False


def require_user(request: Request):
    if request.url.path in PUBLIC_PATHS:
        return None
    token = request.cookies.get(COOKIE, '')
    rows = db.query('SELECT u.id, u.username FROM sessions s JOIN users u ON u.id=s.user_id WHERE s.token_hash=? AND s.expires_at>?', (digest(token), time.time())) if token else []
    if not rows:
        raise HTTPException(401, 'Please sign in to continue')
    return rows[0]


def require_admin(user=Depends(require_user)):
    if not user or not db.query('SELECT id FROM users WHERE id=? AND is_admin=1', (user['id'],)):
        raise HTTPException(403, 'Administrator access required')
    return user


def limit_attempts(request, username):
    # Persistent buckets survive restarts. Ignore untrusted forwarded headers;
    # uvicorn trusts them only from the configured reverse proxy in production.
    peer = request.client.host if request.client else 'unknown'
    now = time.time()
    keys = [('ip:' + peer, 30), ('name:' + username, 10)]
    with db.tx() as c:
        c.execute('DELETE FROM auth_attempts WHERE started_at < ?', (now - 900,))
        for key, limit in keys:
            row = c.execute('SELECT attempts FROM auth_attempts WHERE key=?', (key,)).fetchone()
            if row and row['attempts'] >= limit:
                raise HTTPException(429, 'Too many sign-in attempts. Try again in 15 minutes.', headers={'Retry-After': '900'})
        for key, _ in keys:
            c.execute('INSERT INTO auth_attempts(key, started_at, attempts) VALUES(?,?,1) ON CONFLICT(key) DO UPDATE SET attempts=attempts+1', (key, now))


class Credentials(BaseModel):
    username: str = Field(min_length=3, max_length=32)
    password: str = Field(min_length=1, max_length=128)


def normalized_username(value):
    value = value.strip().lower()
    if not re.fullmatch(r'[a-z0-9_]{3,32}', value):
        raise HTTPException(400, 'Use 3–32 letters, numbers or underscores for your username')
    return value


def create_session(user, request, response):
    token = secrets.token_urlsafe(32)
    with db.tx() as c:
        c.execute('DELETE FROM sessions WHERE expires_at <= ? OR token_hash=?', (time.time(), digest(request.cookies.get(COOKIE, ''))))
        c.execute('INSERT INTO sessions(token_hash,user_id,expires_at) VALUES(?,?,?)', (digest(token), user['id'], time.time() + SESSION_SECONDS))
    response.set_cookie(COOKIE, token, max_age=SESSION_SECONDS, httponly=True, secure=SECURE_COOKIE, samesite='lax', path='/api')
    response.headers['Cache-Control'] = 'no-store'
    return {'id': user['id'], 'username': user['username']}


@router.post('/register', status_code=201)
def register(body: Credentials, request: Request, response: Response):
    username = normalized_username(body.username)
    limit_attempts(request, username)
    if len(body.password) < 8:
        raise HTTPException(400, 'Use at least 8 characters for your password')
    password_hash = hash_password(body.password)
    try:
        with db.tx() as c:
            row = c.execute('INSERT INTO users(username,password_hash,created_at) VALUES(?,?,?)', (username, password_hash, time.time()))
            user = {'id': row.lastrowid, 'username': username}
    except sqlite3.IntegrityError:
        raise HTTPException(409, 'That username is unavailable') from None
    return create_session(user, request, response)


@router.post('/login')
def login(body: Credentials, request: Request, response: Response):
    username = normalized_username(body.username)
    limit_attempts(request, username)
    rows = db.query('SELECT id, username, password_hash FROM users WHERE username=?', (username,))
    valid = verify_password(body.password, rows[0]['password_hash'] if rows else DUMMY_HASH)
    if not rows or not valid:
        raise HTTPException(401, 'Incorrect username or password')
    return create_session(rows[0], request, response)


@router.get('/me')
def me(user=Depends(require_user)):
    return user


@router.post('/logout')
def logout(request: Request, response: Response, user=Depends(require_user)):
    with db.tx() as c:
        c.execute('DELETE FROM sessions WHERE token_hash=?', (digest(request.cookies.get(COOKIE, '')),))
    response.delete_cookie(COOKIE, path='/api', httponly=True, secure=SECURE_COOKIE, samesite='lax')
    return {'ok': True}
