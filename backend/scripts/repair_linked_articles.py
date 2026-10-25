"""Back up and repair local HN content; preserve all saved user records. No AI calls."""
import json
import sqlite3
import sys
import time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from app import db, linked_content
from app.ingest import extract_article


def main():
    backup = db.DB_PATH.with_name(f'finite-before-linked-repair-{int(time.time())}.sqlite3')
    with db.connect() as source, sqlite3.connect(backup) as destination:
        source.backup(destination)
    rows = db.query("SELECT * FROM articles WHERE source_id='hackernews'")
    ids = {row['id'] for row in rows}
    stories = [s for s in db.query('SELECT id,article_ids FROM stories') if ids.intersection(json.loads(s['article_ids']))]
    with db.tx() as c:
        for s in stories:
            c.execute("UPDATE stories SET analysis=NULL, translations='{}' WHERE id=?", (s['id'],))
    print('Backup:', backup, flush=True)
    for a in rows:
        key = f"linked-content-v{linked_content.VERSION}:" + a["id"]
        cached = db.kv_get(key)
        if cached and cached.get("status") == "unavailable":
            db.kv_set(key, linked_content.resolve(a))
        text = extract_article(a)
        print(a['id'], 'available' if text else 'unavailable', a['title'], flush=True)
    print(f'Repaired {len(rows)} articles; invalidated {len(stories)} story caches. All user records preserved.')

if __name__ == '__main__':
    main()
