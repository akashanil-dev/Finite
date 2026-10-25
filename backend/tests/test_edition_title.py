import unittest
from unittest.mock import patch
from app import edition_title


class EditionTitleTests(unittest.TestCase):
    def test_read_never_generates_and_fallback_uses_actual_headlines(self):
        stories=[{'id':'a','title':'NASA tests a Moon lander'},{'id':'b','title':'Kerala issues rain warnings'}]
        with patch.object(edition_title,'context',return_value=stories), patch.object(edition_title.db,'kv_get',return_value=None), patch.object(edition_title.llm,'chat_json') as chat:
            self.assertEqual(edition_title.cover_line(['a','b']), 'NASA tests a Moon lander / Kerala issues rain warnings')
            chat.assert_not_called()

    def test_generation_is_saved_with_evidence_and_reused(self):
        stories=[{'id':'a','title':'NASA tests a Moon lander'},{'id':'b','title':'Kerala issues rain warnings'}]
        result={'title':'Moon lander tests and rain warnings in Kerala','story_ids':['a','b']}
        with patch.object(edition_title,'context',return_value=stories), patch.object(edition_title.db,'kv_get',return_value=None), patch.object(edition_title.db,'kv_set') as save, patch.object(edition_title.llm,'chat_json',return_value=result):
            self.assertEqual(edition_title.cover_line(['a','b'],generate=True),result['title'])
            save.assert_called_once()
        with patch.object(edition_title,'context',return_value=stories), patch.object(edition_title.db,'kv_get',return_value=result), patch.object(edition_title.llm,'chat_json') as chat:
            self.assertEqual(edition_title.cover_line(['a','b']),result['title']);chat.assert_not_called()
        self.assertNotEqual(edition_title.cache_key(stories),edition_title.cache_key(stories[:1]))

    def test_invalid_support_is_rejected(self):
        with patch.object(edition_title,'context',return_value=[{'id':'a','title':'A real headline'}]), patch.object(edition_title.db,'kv_get',return_value=None), patch.object(edition_title.db,'kv_set') as save, patch.object(edition_title.llm,'chat_json',return_value={'title':'An invented cover line','story_ids':[{}]}):
            self.assertEqual(edition_title.cover_line(['a'],generate=True),'A real headline')
            save.assert_not_called()
