"""Synthetic regressions for research coverage, attribution and access status."""
import unittest
from validate_pack import validate_company_research, company_research_status


def ledger():
    return {
        'checked_at': '2026-09-15', 'mode': 'searched', 'exception_reason': '',
        'sources': [{'id': 's1', 'pointer': 'https://example.com/company', 'kind': 'official',
                     'accessed_at': '2026-09-15', 'published_at': None, 'updated_at': None,
                     'date_evidence': ''}],
        'searches': [{'id': 'q1', 'query': 'Example Company identity and recent announcements',
                      'outcome': 'read', 'source_ids': ['s1']}],
        'topics': {name: {'status': 'supported', 'finding': 'A bounded finding for ' + name,
                         'source_ids': ['s1'], 'search_ids': ['q1'],
                         'evidence': [{'source_id': 's1', 'locator': 'Company introduction paragraph',
                                       'excerpt': 'Example Company operates a retail service.'}]}
                   for name in ('identity', 'scale_and_model', 'recent_developments',
                                'conflicts', 'interview_implications')},
    }


class CompanyResearchTests(unittest.TestCase):
    def test_complete(self):
        data = ledger()
        self.assertEqual(validate_company_research(data), [])
        self.assertEqual(company_research_status(data), 'searched')

    def test_missing_topic(self):
        data = ledger()
        del data['topics']['identity']
        self.assertTrue(validate_company_research(data))

    def test_missing_precise_evidence(self):
        data = ledger()
        data['topics']['identity']['evidence'] = []
        self.assertTrue(validate_company_research(data))

    def test_evidence_must_reference_topic_source(self):
        data = ledger()
        data['topics']['identity']['evidence'][0]['source_id'] = 'other'
        self.assertTrue(validate_company_research(data))

    def test_known_dates_require_observed_label(self):
        data = ledger()
        data['sources'][0]['updated_at'] = '2026-09-01'
        self.assertTrue(validate_company_research(data))
        data['sources'][0]['date_evidence'] = 'Footer: Updated 2026-09-01'
        self.assertEqual(validate_company_research(data), [])
        self.assertIsNone(data['sources'][0]['published_at'])

    def test_all_blocked_must_not_claim_searched(self):
        data = ledger()
        data['searches'][0].update(outcome='blocked', source_ids=[])
        for topic in data['topics'].values():
            topic.update(status='blocked', source_ids=[], evidence=[])
        self.assertTrue(validate_company_research(data))
        data.update(mode='unavailable', exception_reason='Search service returned access errors')
        self.assertEqual(validate_company_research(data), [])
        self.assertEqual(company_research_status(data), 'unavailable')

    def test_no_results_is_valid_with_gaps(self):
        data = ledger()
        data['sources'] = []
        data['searches'][0].update(outcome='no-results', source_ids=[])
        for topic in data['topics'].values():
            topic.update(status='not-found', source_ids=[], evidence=[])
        self.assertEqual(validate_company_research(data), [])
        self.assertEqual(company_research_status(data), 'searched-with-gaps')

    def test_explicit_no_browsing_exception(self):
        data = ledger()
        data.update(mode='provided-only', exception_reason='User requested supplied sources only', searches=[])
        for topic in data['topics'].values():
            topic['search_ids'] = []
        self.assertEqual(validate_company_research(data), [])
        self.assertEqual(company_research_status(data), 'provided-only')
        data['exception_reason'] = ''
        self.assertTrue(validate_company_research(data))

    def test_dangling_search_source(self):
        data = ledger()
        data['searches'][0]['source_ids'] = ['missing']
        self.assertTrue(validate_company_research(data))


if __name__ == '__main__':
    unittest.main()
