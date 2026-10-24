import unittest
from unittest.mock import patch
from app import rabbithole, translate


class ValidationTests(unittest.TestCase):
    def test_verifier_fails_closed(self):
        nodes = [{'text': 'A claim', 'citations': ['A1']}]
        passages = [{'ref': 'A1', 'text': 'Evidence'}]
        for result in [None, {}, {'results': 'bad'}, {'results': [{'i':0,'supported':True},{'i':0,'supported':False}]}, {'results':[{'i':0,'supported':'true'}]}]:
            with patch.object(rabbithole.llm, 'chat_json', return_value=result):
                self.assertEqual(rabbithole._verify(nodes, passages), ([], 1))
        with patch.object(rabbithole.llm, 'chat_json', return_value={'results':[{'i':0,'supported':True}]}):
            self.assertEqual(rabbithole._verify(nodes, passages), (nodes, 0))

    def test_translation_requires_nonempty_strings(self):
        for result in [{'t':[None]}, {'t':'x'}, {'t':['']}, {'t':[{}]}]:
            with patch.object(translate.llm, 'chat_json', return_value=result):
                self.assertEqual(translate.translate_payload({'title':'Example'}, 'ml')['translation'], 'unavailable')

    def test_timeline_dates_are_verified_and_unsupported_events_removed(self):
        import json
        import tempfile
        from pathlib import Path
        from app import db
        with tempfile.TemporaryDirectory() as folder, patch.object(db, 'DB_PATH', Path(folder) / 'test.db'):
            db.init()
            with db.tx() as conn:
                conn.execute("INSERT INTO stories(id,article_ids,title,lang,subfields,created_at) VALUES('s','[]','Story','en','{}',0)")
            payload = {'nodes': [], 'timeline': [{'date':'2099', 'event':'An unsupported event', 'citations':['A1']}], 'next_questions': []}
            source = {'ref':'A1', 'text':'No such event', 'name':'Source', 'title':'Title'}
            analysis = {'summary':{'standard':'Summary'}, 'concepts':[]}
            with patch.object(rabbithole, 'analyze', return_value=analysis), patch.object(rabbithole, 'gather', return_value=[source]), patch.object(rabbithole.llm, 'chat_json', side_effect=[payload, {'results':[{'i':0,'supported':False}]}]) as chat:
                result = rabbithole.explore('s','Why?',angle='history')
                self.assertEqual(result['timeline'], [])
                self.assertEqual(result['dropped_claims'], 1)
                self.assertTrue(result['insufficient'])
                self.assertIn('2099: An unsupported event', chat.call_args.args[1])
