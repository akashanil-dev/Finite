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

    def set_origin(self, title, concepts, description=''):
        with db.tx() as c:
            c.execute('UPDATE stories SET title=?, analysis=? WHERE id=?', (title, json.dumps({'concepts': concepts}), 's'))
            c.execute('UPDATE articles SET title=?, description=? WHERE id=?', (title, description or title, '0'))

    def test_kerala_report_rejects_screenshot_matches(self):
        # User-reported headline; descriptions below are synthetic regression fixtures.
        title = 'Kerala University VC says no move to ban student politics, stresses need to curb violence'
        self.set_origin(title, ['There', 'Responding'], 'There should be no violence. Responding to questions, the VC discussed student politics.')
        for i, headline in enumerate([
            'Google Play System update latest Version download: How to check updates and fix the January 2027 date',
            "Ever heard of a touchscreen garment? World's 1st is here - washable, breathable",
            "Forget iPhone Duo: Ashwini Vaishnaw sets October 2028 deadline for India’s own smartphone brand",
        ], 1):
            self.add_story(i, headline)
            with db.tx() as c:
                c.execute('UPDATE articles SET description=? WHERE id=?', ('There is an update. Responding to questions, officials explained the announcement.', str(i)))
        self.assertEqual(connections.explore('s')['connections'], [])
        self.add_story(4, 'Kerala University reviews student politics rules to prevent violence')
        result = connections.explore('s')['connections']
        self.assertEqual([r['story_id'] for r in result], ['s4'])
        self.assertEqual(result[0]['concept'], 'Kerala University')

    def test_entity_alone_and_incidental_mentions_are_insufficient(self):
        self.set_origin('Apple launches satellite emergency messaging for phones', ['Apple'])
        self.add_story(1, 'Apple reports quarterly earnings and revenue growth')
        self.add_story(2, 'Satellite emergency messaging arrives on rival phones')
        with db.tx() as c:
            c.execute('UPDATE articles SET description=? WHERE id=?', ('Apple also has satellite emergency messaging.', '2'))
        self.assertEqual(connections.explore('s')['connections'], [])
        self.add_story(3, 'Apple expands satellite emergency messaging to new regions')
        self.assertEqual(connections.explore('s')['connections'][0]['story_id'], 's3')

    def test_relevance_ranked_before_recent_limit(self):
        self.set_origin('OpenAI releases research on medical diagnosis safety', ['OpenAI'])
        self.add_story(1, 'OpenAI medical diagnosis research examines safety')
        for i in range(2, 6):
            self.add_story(i, 'OpenAI releases research on unrelated products')
        result = connections.explore('s')['connections']
        self.assertEqual(result[0]['story_id'], 's1')
        self.assertEqual(len(result), 3)

    def test_sentence_starters_and_cached_variants_filtered(self):
        from app.analysis import proper_nouns
        self.assertEqual(proper_nouns('There is news. Responding to questions. Meanwhile things happen.'), [])
        self.set_origin('There are updates. Responding to news.', ['there', 'THERE', 'Responding', 'Meanwhile'])
        self.add_story(1, 'There are updates. Responding to news.')
        self.assertEqual(connections.explore('s')['connections'], [])

    def test_language_and_topic_exclusions_still_apply(self):
        self.add_story(1)
        with db.tx() as c:
            c.execute("UPDATE stories SET lang='ml' WHERE id='s1'")
        self.assertEqual(connections.explore('s')['connections'], [])
        with db.tx() as c:
            c.execute("UPDATE stories SET lang='en', subfields=? WHERE id='s1'", (json.dumps({'technology':1}),))
        db.kv_set('profile', {'excluded_subfields':['technology']})
        self.assertEqual(connections.explore('s')['connections'], [])
