import json
from unittest.mock import patch
import unittest
import tempfile
from pathlib import Path
from app import connections, db


class ConnectionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        patcher = patch.object(db, 'DB_PATH', Path(self.temp.name) / 'test.db')
        patcher.start()
        self.addCleanup(patcher.stop)
        db.init()
        self.add_story(0)
        with db.tx() as c:
            c.execute("UPDATE stories SET id='s' WHERE id='s0'")
        with db.tx() as c:
            c.execute('UPDATE stories SET analysis=? WHERE id=?', (json.dumps({'concepts': ['OpenAI', 'During']}), 's'))

    def add_story(self, i, text='OpenAI released a new product today.', source='indianexpress'):
        with db.tx() as c:
            c.execute('INSERT INTO articles(id,source_id,lang,title,url,description,fetched_at) VALUES(?,?,?,?,?,?,?)', (str(i), source, 'en', text, f'https://example.org/{i}', text, 0))
            c.execute('INSERT INTO stories(id,article_ids,title,lang,subfields,created_at) VALUES(?,?,?,?,?,?)', (f's{i}', json.dumps([str(i)]), text, 'en', '{}', i))

    def test_literal_evidence_and_finite_results(self):
        for i in range(1, 6):
            self.add_story(i)
        result = connections.explore('s')
        self.assertEqual(len(result['connections']), 3)
        self.assertEqual(result['connections'][0]['concept'], 'OpenAI')
        self.assertEqual(len(result['connections'][0]['evidence']), 2)

    def test_no_substrings_or_invented_mentions(self):
        self.add_story(1, 'OpenAIish names cannot establish a match here.')
        self.assertEqual(connections.explore('s')['connections'], [])
        self.assertIsNone(connections.explore('missing'))

    def test_exclusions_and_duplicate_articles(self):
        self.add_story(1)
        db.kv_set('profile', {'excluded_sources': ['indianexpress']})
        self.assertEqual(connections.explore('s')['connections'], [])
        db.kv_set('profile', {})
        with db.tx() as c:
            c.execute('UPDATE stories SET article_ids=? WHERE id=?', ('["0"]', 's1'))
        self.assertEqual(connections.explore('s')['connections'], [])

    def test_connections_endpoint_no_spending(self):
        from auth_helpers import authenticated_client
        from app.main import app
        self.add_story(1)
        with patch('app.llm.chat_json', side_effect=AssertionError('No AI')), patch('app.budget.reserve', side_effect=AssertionError('No spending')):
            client = authenticated_client(self)
            self.assertEqual(client.get('/api/stories/s/connections').status_code, 200)
            self.assertEqual(client.get('/api/stories/missing/connections').status_code, 404)
