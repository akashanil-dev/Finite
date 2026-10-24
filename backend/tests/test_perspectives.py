import unittest
from unittest.mock import patch

from app import perspectives as p


def article(id, source):
    return {"id": id, "source_id": source, "title": "Council approves a new park", "description": "The council approved a new park at its meeting on Tuesday.", "content": None, "url": "https://example.org/" + id}


class PerspectiveTests(unittest.TestCase):
    def compare(self, articles, responses):
        with patch.object(p.db, "query", side_effect=[[{"article_ids": '["1", "2"]'}], articles]), patch.object(p.llm, "chat_json", side_effect=responses):
            return p.compare("story")

    def test_extractive_and_publisher_dedup(self):
        out = self.compare([article("1", "thehindu_national"), article("2", "thehindu_kerala"), article("3", "hackernews")], [])
        self.assertEqual(out["total_outlets"], 1)
        self.assertEqual(out["status"], "insufficient_sources")
        self.assertTrue(out["outlets"][0]["excerpt"])

    def test_no_key_fallback(self):
        out = self.compare([article("1", "indianexpress"), article("2", "scroll")], [None])
        self.assertEqual(out["mode"], "extractive")
        self.assertEqual(len(out["outlets"]), 2)

    def test_verification_failures_and_success(self):
        claim = {"text": "The council approved a park.", "category": "established", "citations": ["P1", "P2"]}
        for verdict, mode in [(None, "extractive"), ({"results": []}, "extractive"), ({"results": [{"i": 0, "supported": False}]}, "extractive"), ({"results": [{"i": 0, "supported": True}]}, "ai")]:
            with self.subTest(verdict=verdict):
                out = self.compare([article("1", "indianexpress"), article("2", "scroll")], [{"claims": [claim]}, verdict])
                self.assertEqual(out["mode"], mode)

    def test_invalid_citations_and_categories(self):
        base = {"text": "A claim", "category": "reported", "citations": ["P1"]}
        for override in [{"citations": ["fake"]}, {"citations": []}, {"category": "established"}, {"category": "disputed"}, {"category": "bias"}, {"category": []}, {"text": None}]:
            self.assertEqual(p._claims({"claims": [{**base, **override}]}, {"P1"}), [])

    def test_short_lead_sentence_is_preserved(self):
        a = article("1", "indianexpress")
        a["description"] = "The vote passed. Residents welcomed the proposal after a long debate."
        out = self.compare([a], [])
        self.assertEqual(out["outlets"][0]["excerpt"], "The vote passed.")

    def test_missing_story(self):
        with patch.object(p.db, "query", return_value=[]):
            self.assertIsNone(p.compare("missing"))

class PerspectiveRouteTests(unittest.TestCase):
    def test_route_success_and_missing_story(self):
        from auth_helpers import authenticated_client
        from app.main import app
        client = authenticated_client(self)  # No lifespan: no scheduler or live ingestion in tests.
        payload = {"mode": "extractive", "status": "source_comparison", "outlets": [], "total_outlets": 2, "claims": []}
        with patch('app.main.perspectives.compare', return_value=payload):
            response = client.get('/api/stories/test/perspectives')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json(), payload)
        with patch('app.main.perspectives.compare', return_value=None):
            self.assertEqual(client.get('/api/stories/missing/perspectives').status_code, 404)


if __name__ == "__main__":
    unittest.main()
