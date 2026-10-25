import unittest
from unittest.mock import patch
from app import linked_content as lc, analysis

class LinkedContentTests(unittest.TestCase):
    def article(self):
        return {'url':'https://example.com/post', 'description':'Article URL: https://gitlab.com/user/project Comments URL: https://news.ycombinator.com/item?id=1 Points: 21 # Comments: 4'}

    def test_repository_uses_readme_and_preserves_discussion(self):
        with patch.object(lc, 'fetch', return_value=('This project documents its own design. ' * 12, 'text/plain')) as fetch:
            result = lc.resolve(self.article())
        self.assertEqual(result['status'], 'available')
        self.assertIn('/user%2Fproject/', fetch.call_args.args[0])
        self.assertEqual(result['discussion_url'], 'https://news.ycombinator.com/item?id=1')

    def test_metadata_empty_and_fetch_failure_are_not_evidence(self):
        for text in ['', 'Article URL: https://example.com ' * 30, 'Verify you are human ' * 30]:
            with patch.object(lc, 'fetch', return_value=(text, 'text/plain')):
                self.assertEqual(lc.resolve(self.article())['content'], '')
        with patch.object(lc, 'fetch', side_effect=ValueError('blocked')):
            self.assertEqual(lc.resolve(self.article())['status'], 'unavailable')

    def test_private_destinations_rejected(self):
        for addr in ['127.0.0.1', '::1', '169.254.169.254', '10.0.0.1']:
            with patch.object(lc.socket, 'getaddrinfo', return_value=[(0,0,0,'',(addr,80))]):
                with self.assertRaises(ValueError): lc.public_url('https://example.com')
        for url in ['file:///etc/passwd', 'https://user:password@example.com', 'https://example.com:8000']:
            with self.assertRaises(ValueError): lc.public_url(url)

    def test_self_post_does_not_scrape_comments(self):
        with patch.object(lc, 'fetch') as fetch:
            result = lc.resolve({'url':'https://news.ycombinator.com/item?id=1','description':''})
        fetch.assert_not_called()
        self.assertEqual(result['status'], 'unavailable')

    def test_no_content_has_no_facts_or_suggestions(self):
        out = analysis._extractive({'story_type':'general'}, [{'content':'','description':''}])
        self.assertTrue(out['content_unavailable'])
        self.assertEqual(out['what_happened'], [])
        self.assertEqual(out['questions'], [])

    def test_readme_preview_excludes_code_tables_and_markup(self):
        result = lc.readme_prose('# Title\n\nA **documented** project with [limits](docs.md).\n| table | value |\n```sh\nrun-command\n```')
        self.assertEqual(result, 'A documented project with limits.')

    def test_redirect_cannot_reach_private_address(self):
        import httpx
        response = httpx.Response(302, headers={'location':'http://127.0.0.1/admin'}, request=httpx.Request('GET','https://example.com'))
        with patch.object(lc, 'public_url', side_effect=['93.184.216.34', ValueError('private')]), patch.object(lc.httpx, 'Client') as client:
            client.return_value.__enter__.return_value.stream.return_value.__enter__.return_value = response
            with self.assertRaises(ValueError): lc.fetch('https://example.com')
            self.assertEqual(client.call_count, 1)

    def test_empty_first_source_does_not_hide_readable_second_source(self):
        result = analysis._extractive({'story_type':'general', 'title':'Example'}, [{'content':'','description':''}, {'content':'A readable source describes this project.', 'description':''}])
        self.assertIn('readable source', result['summary']['standard'])
        self.assertEqual(result['what_happened'][0]['citations'], ['A2'])
