import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from concurrent.futures import ThreadPoolExecutor
from fastapi import HTTPException
from app import db, briefing, main
from auth_helpers import authenticated_client


class BriefingHistoryTests(unittest.TestCase):
    def setUp(self):
        folder = tempfile.TemporaryDirectory()
        self.addCleanup(folder.cleanup)
        path = patch.object(db, 'DB_PATH', Path(folder.name) / 'test.db')
        path.start(); self.addCleanup(path.stop)
        db.init()
        self.client = authenticated_client(self)

    def insert(self, user=1, parent=None, scheduled=None):
        with db.tx() as c:
            return c.execute("INSERT INTO briefings(created_at,window_start,window_end,config,story_ids,user_id,edition_of,scheduled_for) VALUES(1,0,1,?,'[]',?,?,?)", (json.dumps(briefing.DEFAULT_PROFILE),user,parent,scheduled)).lastrowid

    def test_history_is_owned_paginated_and_preserves_older_editions(self):
        own = [self.insert() for _ in range(23)]
        self.insert(user=2)
        first = self.client.get('/api/briefings').json()
        second = self.client.get('/api/briefings',params={'before': first['next_cursor']}).json()
        self.assertEqual([x['id'] for x in first['items']+second['items']],list(reversed(own)))
        self.assertIsNone(second['next_cursor'])
        self.assertEqual(self.client.get(f'/api/briefings/{own[0]}').status_code,200)

    def test_refresh_is_once_and_cannot_chain_or_replace_original(self):
        original = self.insert()
        with patch.object(main,'do_ingest') as ingest, patch.object(main,'make_briefing',side_effect=lambda user_id, **kw:self.insert(user_id,kw.get('edition_of'))):
            result = self.client.post(f'/api/briefings/{original}/edition')
            self.assertEqual(result.status_code,200)
            child=result.json()['id']
            self.assertFalse(result.json()['can_refresh'])
            self.assertEqual(result.json()['edition_of'],original)
            self.assertEqual(self.client.post(f'/api/briefings/{original}/edition').status_code,409)
            self.assertEqual(self.client.post(f'/api/briefings/{child}/edition').status_code,409)
            self.assertEqual(self.client.post('/api/briefings').status_code,409)
            ingest.assert_called_once()
        self.assertEqual(len(self.client.get('/api/briefings').json()['items']),2)
        self.assertEqual(self.client.get(f'/api/briefings/{original}').status_code,200)

    def test_empty_refresh_is_consumed_and_cross_account_is_denied(self):
        original=self.insert(); other=self.insert(user=2)
        with patch.object(main,'do_ingest') as ingest, patch.object(main,'make_briefing',return_value=None):
            self.assertEqual(self.client.post(f'/api/briefings/{other}/edition').status_code,404)
            self.assertEqual(self.client.post(f'/api/briefings/{original}/edition').status_code,404)
            self.assertFalse(self.client.get(f'/api/briefings/{original}').json()['can_refresh'])
            self.assertEqual(self.client.post(f'/api/briefings/{original}/edition').status_code,409)
            ingest.assert_called_once()

    def test_atomic_claim_allows_only_one_concurrent_refresh(self):
        original=self.insert()
        def run():
            try: return main.extra_edition(original,user={'id':1})
            except HTTPException as e: return e.status_code
        with patch.object(main,'do_ingest') as ingest, patch.object(main,'make_briefing',return_value=None):
            with ThreadPoolExecutor(2) as pool: results=list(pool.map(lambda _:run(),range(2)))
            self.assertEqual(sorted(results),[404,409])
            ingest.assert_called_once()

    def test_initial_creation_is_not_an_unlimited_refresh_endpoint(self):
        with patch.object(main,'do_ingest') as ingest, patch.object(main,'make_briefing',side_effect=lambda user_id:self.insert(user_id)):
            self.assertEqual(self.client.post('/api/briefings').status_code,200)
            self.assertEqual(self.client.post('/api/briefings').status_code,409)
            ingest.assert_called_once()

    def test_schedule_unique_per_user_day_and_migration_idempotent(self):
        self.insert(scheduled='2026-10-25')
        self.insert(user=2,scheduled='2026-10-25')
        import sqlite3
        with self.assertRaises(sqlite3.IntegrityError): self.insert(scheduled='2026-10-25')
        db.init()
        self.assertEqual(len(db.query('SELECT id FROM briefings')),2)

    def test_midnight_delivery_prepares_on_previous_date(self):
        from datetime import datetime
        from zoneinfo import ZoneInfo
        profile={**briefing.DEFAULT_PROFILE,'delivery_time':'00:05','timezone':'Asia/Kolkata'}
        with patch.object(main,'PREPARE_BEFORE_MIN',15):
            self.assertEqual(main.due_schedule(profile,datetime(2026,10,25,23,55,tzinfo=ZoneInfo('Asia/Kolkata'))),'2026-10-26')
            self.assertEqual(main.due_schedule(profile,datetime(2026,10,26,0,1,tzinfo=ZoneInfo('Asia/Kolkata'))),'2026-10-26')

    def test_delivery_waits_for_the_preparation_window(self):
        from datetime import datetime
        from zoneinfo import ZoneInfo
        profile={**briefing.DEFAULT_PROFILE,'delivery_time':'08:00','timezone':'Asia/Kolkata'}
        with patch.object(main,'PREPARE_BEFORE_MIN',15):
            self.assertIsNone(main.due_schedule(profile,datetime(2026,10,25,7,30,tzinfo=ZoneInfo('Asia/Kolkata'))))
            self.assertEqual(main.due_schedule(profile,datetime(2026,10,25,7,50,tzinfo=ZoneInfo('Asia/Kolkata'))),'2026-10-25')
