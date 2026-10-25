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

    def test_unverified_summary_falls_back_but_valid_questions_survive(self):
        from app import analysis
        data={'summary':{'quick':'Made up.','standard':'Supported.','deep':'Supported.'},'what_happened':[],
              'questions':[{'question':'Why did the university review its rules?','angle':'context','search':['University governance']}],
              'missing_piece':[], 'concepts':['University governance']}
        arts=[{'content':'The university reviewed its campus rules after a court direction.', 'description':''}]
        with patch.object(analysis.llm,'chat_json',return_value={'results':[{'i':i,'supported':i!=0} for i in range(4)]}):
            out=analysis._checked_analysis(data,arts)
        self.assertNotEqual(out['summary']['quick'],'Made up.')
        self.assertEqual(len(out['questions']),1)

    def test_malformed_analysis_and_unreviewed_questions_rejected(self):
        from app import analysis
        self.assertIsNone(analysis._checked_analysis({'summary':{'quick':None}},[]))
        data={'summary':dict.fromkeys(['quick','standard','deep'],'Test.'),'questions':[{'question':'Why?','angle':'context'}]}
        with patch.object(analysis.llm,'chat_json',return_value={}):
            self.assertIsNone(analysis._checked_analysis(data,[]))

    def test_extractive_followups_do_not_promote_capitalized_words(self):
        out=rabbithole._extractive('Why?', 'context', [{'text':'There is a question. Responding to it takes time.', 'title':'Example','ref':'A1','kind':'news'}],1,[])
        self.assertEqual(out['next_questions'],[])
        self.assertTrue(out['insufficient'])
