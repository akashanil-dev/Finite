import json
import tempfile
import time
import unittest
from pathlib import Path
from unittest.mock import patch

from fastapi.testclient import TestClient
from app import auth, briefing, db
from app.main import app


class AuthTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        p = patch.object(db, 'DB_PATH', Path(self.temp.name) / 'auth.db')
        p.start()
        self.addCleanup(p.stop)
        db.init()
        self.client = self.new_client()
        self.addCleanup(self.client.close)
        self.no_ai = patch('app.budget.reserve', side_effect=AssertionError('No AI budget permitted'))
        self.no_ai.start()
        self.addCleanup(self.no_ai.stop)

    def new_client(self):
        return TestClient(app, headers={'X-Finite-Request': '1', 'Origin': 'http://localhost:3000'})

    def register(self, client=None, username='alice'):
        client = client or self.client
        response = client.post('/api/auth/register', json={'username': username, 'password': 'simplepassword'})
        self.assertEqual(response.status_code, 201, response.text)
        return response.json()

    def test_registration_hash_cookie_and_duplicate(self):
        user = self.register(username='Alice')
        self.assertEqual(user['username'], 'alice')
        stored = db.query('SELECT password_hash FROM users')[0]['password_hash']
        self.assertNotIn('simplepassword', stored)
        self.assertTrue(auth.verify_password('simplepassword', stored))
        token = self.client.cookies.get(auth.COOKIE)
        self.assertNotEqual(db.query('SELECT token_hash FROM sessions')[0]['token_hash'], token)
        self.assertEqual(self.client.get('/api/auth/me').json()['id'], user['id'])
        duplicate = self.client.post('/api/auth/register', json={'username': 'ALICE', 'password': 'simplepassword'})
        self.assertEqual(duplicate.status_code, 409)
        self.assertEqual(self.client.post('/api/auth/register', json={'username': 'other', 'password': 'short'}).status_code, 400)

    def test_session_logout_expiry_and_invalid_password(self):
        self.register()
        old = self.client.cookies.get(auth.COOKIE)
        self.assertEqual(self.client.post('/api/auth/logout').status_code, 200)
        self.assertEqual(self.client.get('/api/profile').status_code, 401)
        self.client.cookies.set(auth.COOKIE, old, path='/api')
        self.assertEqual(self.client.get('/api/auth/me').status_code, 401)
        self.client.cookies.clear()
        self.assertEqual(self.client.post('/api/auth/login', json={'username': 'alice', 'password': 'wrong'}).status_code, 401)
        login = self.client.post('/api/auth/login', json={'username': 'ALICE', 'password': 'simplepassword'})
        self.assertEqual(login.status_code, 200)
        self.assertIn('HttpOnly', login.headers['set-cookie'])
        self.assertIn('SameSite=lax', login.headers['set-cookie'])
        self.assertNotEqual(self.client.cookies.get(auth.COOKIE), old)
        with db.tx() as c:
            c.execute('UPDATE sessions SET expires_at=0')
        self.assertEqual(self.client.get('/api/auth/me').status_code, 401)

    def test_private_data_isolation_and_legacy_preservation(self):
        alice = self.register()
        bob = self.new_client()
        self.addCleanup(bob.close)
        b = self.register(bob, 'bob')
        profile = self.client.get('/api/profile').json()
        profile.update(onboarded=True, interests={'ai': 3})
        self.assertEqual(self.client.put('/api/profile', json=profile).status_code, 200)
        self.assertFalse(bob.get('/api/profile').json()['onboarded'])
        with db.tx() as c:
            c.execute("INSERT INTO stories(id,article_ids,title,lang,subfields,created_at) VALUES('s','[]','Story','en','{}',0)")
            for owner in [None, alice['id'], b['id']]:
                c.execute('INSERT INTO briefings(created_at,window_start,window_end,config,story_ids,user_id) VALUES(0,0,0,?,?,?)', (json.dumps(briefing.DEFAULT_PROFILE), '["s"]', owner))
        self.assertEqual(self.client.get('/api/briefings/latest').json()['id'], 2)
        self.assertEqual(bob.get('/api/briefings/2').status_code, 404)
        self.assertEqual(self.client.get('/api/briefings/1').status_code, 404)
        self.assertEqual(bob.post('/api/briefings/2/read', json={'story_id': 's'}).status_code, 404)
        self.assertEqual(self.client.post('/api/briefings/2/read', json={'story_id': 'unrelated'}).status_code, 404)
        self.assertEqual(self.client.post('/api/briefings/2/read', json={'story_id': 's'}).status_code, 200)
        self.assertEqual(bob.get('/api/passport').json()['briefings_completed'], 0)
        self.assertEqual(self.client.post('/api/journeys', json={'story_id': 's', 'path': [{'question': 'Private question'}]}).status_code, 200)
        self.assertEqual(len(self.client.get('/api/passport').json()['journeys']), 1)
        self.assertEqual(bob.get('/api/passport').json()['journeys'], [])
        db.init()  # migration is idempotent and doesn't assign legacy records.
        self.assertIsNone(db.query('SELECT user_id FROM briefings WHERE id=1')[0]['user_id'])

    def test_csrf_and_auth_required_on_all_feature_endpoints(self):
        for path in ['/api/profile','/api/passport','/api/briefings/latest','/api/stories/s','/api/stories/s/connections','/api/stories/s/timeline','/api/stories/s/perspectives']:
            self.assertEqual(self.client.get(path).status_code, 401, path)
        self.assertEqual(self.client.get('/api/health').status_code, 200)
        body = {'username': 'alice', 'password': 'simplepassword'}
        self.assertEqual(self.client.post('/api/auth/register', json=body, headers={'Origin': 'https://attacker.example'}).status_code, 403)
        other = TestClient(app)
        self.addCleanup(other.close)
        self.assertEqual(other.post('/api/auth/register', json=body).status_code, 403)
        self.register()
        self.assertEqual(self.client.post('/api/ingest').status_code, 403)
        self.assertEqual(self.client.get('/api/ai-budget').status_code, 403)

    def test_persistent_login_rate_limit(self):
        for _ in range(10):
            result = self.client.post('/api/auth/login', json={'username': 'missing', 'password': 'wrong'})
            self.assertEqual(result.status_code, 401)
        blocked = self.new_client()
        self.addCleanup(blocked.close)
        self.assertEqual(blocked.post('/api/auth/login', json={'username': 'missing', 'password': 'wrong'}).status_code, 429)

    def test_legacy_claim_is_explicit_and_idempotent(self):
        from app.claim_legacy import claim
        user = self.register()
        db.kv_set('profile', {'onboarded': True})
        with db.tx() as c:
            c.execute("INSERT INTO briefings(created_at,window_start,window_end,config,story_ids) VALUES(0,0,0,'{}','[]')")
        self.assertIsNone(self.client.get('/api/briefings/latest').json())
        self.assertEqual(claim('alice')['briefings'], 1)
        self.assertEqual(claim('alice')['briefings'], 0)
        self.assertTrue(briefing.get_profile(user['id'])['onboarded'])
        self.assertIsNotNone(self.client.get('/api/briefings/latest').json())

    def test_briefing_dedup_is_per_user(self):
        alice = self.register()
        bob = self.new_client()
        self.addCleanup(bob.close)
        other = self.register(bob, 'bob')
        with db.tx() as c:
            c.execute("INSERT INTO articles(id,source_id,lang,title,url,description,published_at,updated_at,fetched_at,subfields,story_type,classified) VALUES('a','indianexpress','en','Research report','https://example.org/a','A research report about elections.',?,?,?,?,?,1)", (time.time(),time.time(),time.time(),'{"elections":1}', 'general'))
        profile = {**briefing.DEFAULT_PROFILE, 'interests': {'elections': 3}}
        with patch('app.briefing._cluster', side_effect=lambda articles: [articles]):
            first = briefing.build_briefing(profile, alice['id'])
            second = briefing.build_briefing(profile, other['id'])
        self.assertEqual(len(briefing.briefing_payload(first, alice['id'])['stories']), 1)
        self.assertEqual(len(briefing.briefing_payload(second, other['id'])['stories']), 1)
        self.assertIsNone(briefing.briefing_payload(first, other['id']))

    def test_admin_requires_explicit_local_grant(self):
        from app.manage_user import set_admin
        self.register()
        self.assertEqual(self.client.get('/api/ai-budget').status_code, 403)
        set_admin('alice', True)
        self.assertEqual(self.client.get('/api/ai-budget').status_code, 200)
        set_admin('alice', False)
        self.assertEqual(self.client.get('/api/ai-budget').status_code, 403)

    def test_secure_cookie_production_setting(self):
        with patch.object(auth, 'SECURE_COOKIE', True):
            response = self.client.post('/api/auth/register', json={'username': 'alice', 'password': 'simplepassword'})
        self.assertEqual(response.status_code, 201)
        self.assertIn('Secure', response.headers['set-cookie'])
