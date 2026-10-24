import concurrent.futures
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch, Mock

from app import budget, llm


class BudgetTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.patch = patch.object(budget, 'BUDGET_PATH', Path(self.tmp.name) / 'budget.db')
        self.patch.start()
        self.addCleanup(self.patch.stop)

    def test_concurrent_reservations_never_exceed_cap(self):
        def attempt(_):
            try:
                budget.reserve('gpt-6.1-sol', ['hello'], 4000)
                return True
            except budget.BudgetBlocked:
                return False
        with concurrent.futures.ThreadPoolExecutor(8) as pool:
            results = list(pool.map(attempt, range(30)))
        self.assertTrue(any(results))
        self.assertFalse(all(results))
        self.assertLessEqual(budget.status()['reserved_usd'], 1)
        self.assertEqual(budget.status()['requests'], sum(results))

    def test_unknown_models_and_oversized_requests_block(self):
        for model, text, output in [('unknown', 'a', 1), ('gpt-6-luna', 'a', 12001), ('gpt-6-luna', 'a'*100001, 1)]:
            with self.assertRaises(budget.BudgetBlocked):
                budget.reserve(model, [text], output)
        self.assertEqual(budget.status()['requests'], 0)

    def test_failed_request_retains_reservation_and_cache_is_free(self):
        client = Mock()
        client.responses.create.side_effect = TimeoutError()
        with patch.object(llm, 'MOCK_MODE', False), patch.object(llm, 'LLM_CACHE_DIR', Path(self.tmp.name)), patch.object(llm, '_get_client', return_value=client):
            self.assertIsNone(llm.chat_json('system', 'user'))
            self.assertEqual(budget.status()['requests'], 1)
            path = llm._cache_path('chat', {'s':'system', 'u':'user', 'm':llm.FAST_MODEL})
            path.write_text('{"cached": true}')
            self.assertEqual(llm.chat_json('system', 'user'), {'cached': True})
            self.assertEqual(budget.status()['requests'], 1)
            self.assertEqual(client.responses.create.call_count, 1)

    def test_exhaustion_does_not_call_provider(self):
        with patch.object(budget, 'MAX_CALLS', 1):
            budget.reserve('gpt-6-luna', ['first'], 1)
            with patch.object(llm, 'MOCK_MODE', False), patch.object(llm, 'LLM_CACHE_DIR', Path(self.tmp.name)), patch.object(llm, '_get_client') as client:
                self.assertIsNone(llm.chat_json('system', 'new'))
                self.assertIsNone(llm.embed(['new']))
                client.assert_not_called()


if __name__ == '__main__':
    unittest.main()
