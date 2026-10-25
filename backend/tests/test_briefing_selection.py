import json
import tempfile
import time
import unittest
from pathlib import Path
from unittest.mock import patch

from app import briefing, db


class BriefingSelectionTests(unittest.TestCase):
    def setUp(self):
        folder = tempfile.TemporaryDirectory()
        self.addCleanup(folder.cleanup)
        db_path = patch.object(db, 'DB_PATH', Path(folder.name) / 'test.db')
        db_path.start()
        self.addCleanup(db_path.stop)
        db.init()
        # Selection tests keep grouping deterministic; no embeddings or paid calls.
        cluster = patch.object(briefing, '_cluster', side_effect=lambda articles: [[a] for a in articles])
        cluster.start()
        self.addCleanup(cluster.stop)

    def articles(self, count, topic='kerala', source='thehindu_kerala', age=1):
        now = time.time()
        with db.tx() as c:
            for i in range(count):
                aid = f'{topic}-{source}-{i}'
                c.execute('INSERT INTO articles(id,source_id,lang,title,url,description,published_at,updated_at,fetched_at,subfields,story_type,classified) VALUES(?,?,?,?,?,?,?,?,?,?,?,1)',
                          (aid,source,'en',f'{topic} story {i}',f'https://example.test/{aid}','A source description.',now-age*3600-i,now,now,json.dumps({topic:1}),'general'))

    def build(self, interests, **overrides):
        profile = {**briefing.DEFAULT_PROFILE, 'interests':interests, 'stories_per_briefing':20, **overrides}
        bid = briefing.build_briefing(profile=profile, user_id=1)
        return briefing.briefing_payload(bid,1) if bid else None

    def test_narrow_profile_fills_twenty_instead_of_stopping_at_five(self):
        self.articles(25)
        result = self.build({'kerala':3})
        self.assertEqual(len(result['stories']),20)
        self.assertEqual(result['stories'][0]['title'],'kerala story 0')
        self.assertEqual(result['stories'][-1]['title'],'kerala story 19')
        self.assertEqual(briefing.list_briefings(1)['items'][0]['requested_count'],20)

    def test_diversity_still_gets_first_choice_before_backfill(self):
        self.articles(25)
        self.articles(5,topic='education',age=10)
        result = self.build({'kerala':3,'education':3})
        self.assertEqual(len(result['stories']),20)
        self.assertEqual(sum(s['title'].startswith('education') for s in result['stories']),5)

    def test_backfill_never_reuses_delivered_articles(self):
        self.articles(25)
        first = self.build({'kerala':3})
        second = self.build({'kerala':3})
        self.assertEqual(len(second['stories']),5)
        self.assertFalse({s['id'] for s in first['stories']} & {s['id'] for s in second['stories']})
        self.assertIsNone(self.build({'kerala':3}))

    def test_shortage_is_honest_and_filters_are_not_relaxed(self):
        self.articles(2)
        self.articles(20,source='scroll')
        self.articles(20,topic='education')
        self.articles(20,source='thehindu_national',age=50)
        result = self.build({'kerala':3,'education':3},excluded_sources=['scroll'],excluded_subfields=['education'])
        self.assertEqual(len(result['stories']),2)
        self.assertEqual(briefing.list_briefings(1)['items'][0]['requested_count'],20)

    def test_normal_editions_share_card_features_across_accounts(self):
        self.articles(25)
        profile = {**briefing.DEFAULT_PROFILE, 'interests': {'kerala': 3}, 'stories_per_briefing': 20}
        def cover(system, user, **kwargs):
            return {'title': 'Kerala reports bring a new set of local developments',
                    'story_ids': [s['id'] for s in json.loads(user)[:2]]}
        with patch.object(briefing.llm, 'chat_json', side_effect=cover):
            original = briefing.build_briefing(profile=profile, user_id=1)
            extra = briefing.build_briefing(profile=profile, user_id=1, edition_of=original)
            scheduled = briefing.build_briefing(profile=profile, user_id=2, scheduled_for='2026-10-25')
        with patch.object(briefing.llm, 'chat_json') as generate:
            first = briefing.list_briefings(1)['items']
            second = briefing.list_briefings(2)['items']
            generate.assert_not_called()
        self.assertEqual([b['number'] for b in first], [2, 1])
        self.assertEqual(second[0]['number'], 1)
        for bid, owner in [(original, 1), (extra, 1), (scheduled, 2)]:
            self.assertTrue(briefing.mark_opened(bid, owner))
            self.assertFalse(briefing.mark_opened(bid, 999))
            read = briefing.mark_read(bid, None, owner, read=True)
            self.assertEqual(len(read['read_ids']), len(read['stories']))
            self.assertIsNotNone(read['completed_at'])
            unread = briefing.mark_read(bid, None, owner, read=False)
            self.assertEqual(unread['read_ids'], [])
            self.assertIsNone(unread['completed_at'])
        for item in first + second:
            self.assertEqual(item['headline'], 'Kerala reports bring a new set of local developments')
