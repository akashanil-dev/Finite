import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from app import db, rabbithole


class ExplorationDepthTests(unittest.TestCase):
    def test_cached_depths_preserve_the_endpoint_and_current_path(self):
        with tempfile.TemporaryDirectory() as folder, patch.object(db, 'DB_PATH', Path(folder) / 'test.db'):
            db.init()
            with db.tx() as conn:
                conn.execute("INSERT INTO stories(id,article_ids,title,lang,subfields,story_type,created_at) VALUES(?,?,?,?,?,?,?)", ('s', '[]', 'QA story', 'en', '{}', 'general', 0))
            analysis = {'concepts': [], 'summary': {'standard': 'QA', 'deep': 'QA'}}
            def extractive(question, angle, passages, depth, concepts):
                return {'nodes': [], 'timeline': [], 'next_questions': [] if depth == 2 else [{'question': 'Next?'}]}
            with patch.object(rabbithole, 'MOCK_MODE', True), patch.object(rabbithole, 'analyze', return_value=analysis), patch.object(rabbithole, 'gather', return_value=[]), patch.object(rabbithole.llm, 'chat_json', return_value=None), patch.object(rabbithole, '_extractive', side_effect=extractive) as generate:
                first = rabbithole.explore('s', 'Same question', depth=1)
                final = rabbithole.explore('s', 'Same question', depth=2, path=[{'question': 'Old path'}])
                again = rabbithole.explore('s', 'Same question', depth=2, path=[{'question': 'Current path'}])
                self.assertNotEqual(first['key'], final['key'])
                self.assertEqual(final['depth'], 2)
                self.assertEqual(final['next_questions'], [])
                self.assertEqual(again['path'], [{'question': 'Current path'}])
                self.assertEqual(generate.call_count, 2)
                self.assertTrue(first['next_questions'])

    def test_journey_preserves_optional_prediction(self):
        from auth_helpers import authenticated_client
        from app.main import app
        with tempfile.TemporaryDirectory() as folder, patch.object(db, 'DB_PATH', Path(folder) / 'test.db'):
            db.init()
            with db.tx() as conn:
                conn.execute("INSERT INTO stories(id,article_ids,title,lang,subfields,story_type,created_at) VALUES(?,?,?,?,?,?,?)", ('s', '[]', 'QA story', 'en', '{}', 'general', 0))
            response = authenticated_client(self).post('/api/journeys', json={'story_id': 's', 'path': [{'question': 'Why?'}, {'question': 'Connection?', 'prediction': 'A shared history'}], 'concepts': []})
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json()['journeys'][0]['path'][1]['prediction'], 'A shared history')
