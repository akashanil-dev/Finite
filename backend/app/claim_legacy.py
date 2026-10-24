"""Explicit local-owner migration: uv run python -m app.claim_legacy USERNAME.

Back up the database first. Never expose this operation as an HTTP endpoint.
"""
import argparse
from . import db


def claim(username):
    db.init()
    with db.tx() as c:
        c.execute('BEGIN IMMEDIATE')
        user = c.execute('SELECT id FROM users WHERE username=?', (username.strip().lower(),)).fetchone()
        if not user:
            raise ValueError('Create this account before assigning legacy data')
        user_id = user['id']
        key = f'profile:{user_id}'
        if not c.execute('SELECT 1 FROM kv WHERE key=?', (key,)).fetchone():
            c.execute("INSERT INTO kv(key,value) SELECT ?,value FROM kv WHERE key='profile'", (key,))
        counts = {}
        for table in ('briefings', 'journeys'):
            counts[table] = c.execute(f'UPDATE {table} SET user_id=? WHERE user_id IS NULL', (user_id,)).rowcount
    return counts


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('username')
    args = parser.parse_args()
    try:
        print(claim(args.username))
    except ValueError as exc:
        parser.exit(1, str(exc) + '\n')
