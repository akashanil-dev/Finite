import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from app import db, time_machine as tm


class TimeMachineTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        patcher = patch.object(db, 'DB_PATH', Path(self.temp.name) / 'test.db')
        patcher.start()
        self.addCleanup(patcher.stop)
        db.init()

    def seed(self, texts):
        with db.tx() as c:
            c.execute("INSERT INTO stories(id,article_ids,title,lang,subfields,created_at) VALUES(?,?,?,?,?,?)", ('s', json.dumps([str(i) for i in range(len(texts))]), 'Story', 'en', '{}', 0))
            for i, text in enumerate(texts):
                c.execute('INSERT INTO articles(id,source_id,lang,title,url,description,published_at,updated_at,fetched_at) VALUES(?,?,?,?,?,?,?,?,?)',
                          (str(i), 'indianexpress', 'en', 'Story report', 'https://example.org/' + str(i), text, 1792837800 + i, 1792841400 + i, 1792841400))

    def test_dates_never_infer_year_and_preserve_conflicts(self):
        self.assertEqual(tm.date_info('The strike began on October 12.')['sort_date'], None)
        self.assertEqual(tm.date_info('The reports say 2005 or 2006.')['precision'], 'multiple_dates')
        self.assertEqual(tm.date_info('On 12 October 2026 students started a strike.')['sort_date'], '2026-10-12')
        self.assertEqual(tm.date_info('It happened on February 30, 2026.')['sort_date'], None)
        self.assertIsNone(tm.date_info('It happened yesterday.'))

    def test_citations_deduplication_and_chronology(self):
        sentence = 'The union was suspended in 2005 after campus unrest.'
        self.seed([sentence + ' The strike started on October 12.', sentence + ' Talks resumed on October 24, 2026.'])
        result = tm.timeline('s')
        self.assertEqual(result['events'][0]['date'], '2005')
        self.assertEqual(result['events'][0]['group'], 'background')
        self.assertEqual(result['events'][0]['citations'], ['T1', 'T2'])
        self.assertEqual(result['events'][1]['group'], 'current')
        self.assertEqual(result['events'][2]['group'], 'unresolved')
        self.assertEqual(len(result['coverage']), 2)
        self.assertTrue(result['coverage'][0]['updated_at'])

    def test_finite_output_and_no_fabricated_dates(self):
        self.seed([' '.join(f'The committee met in {year} to discuss policy.' for year in range(2000, 2020))])
        result = tm.timeline('s')
        self.assertEqual(len(result['events']), tm.MAX_EVENTS)
        self.assertEqual(result['total_events'], 20)

    def test_empty_and_missing_story(self):
        self.seed(['There are no dates in this report.'])
        self.assertEqual(tm.timeline('s')['status'], 'no_dated_events')
        self.assertIsNone(tm.timeline('absent'))

    def test_endpoint_never_calls_ai(self):
        from fastapi.testclient import TestClient
        from app.main import app
        self.seed(['The committee was founded in 2001 to oversee elections.'])
        with patch('app.llm.chat_json', side_effect=AssertionError('No AI permitted')), patch('app.budget.reserve', side_effect=AssertionError('No spending permitted')):
            client = TestClient(app)
            self.assertEqual(client.get('/api/stories/s/timeline').status_code, 200)
            self.assertEqual(client.get('/api/stories/absent/timeline').status_code, 404)
