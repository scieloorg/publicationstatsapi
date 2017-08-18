# coding: utf-8
import unittest

from publicationstats import queries


class PublicationStatsQueriesTest(unittest.TestCase):

    def test_journals_stats(self):

        query_result = {
            '_shards': {'failed': 0, 'successful': 5, 'total': 5},
            'aggregations': {
                'status': {
                    'buckets': [
                        {'doc_count': 89, 'key': 'current'},
                        {'doc_count': 30, 'key': 'suspended'},
                        {'doc_count': 24, 'key': 'deceased'},
                        {'doc_count': 4, 'key': 'inprogress'}
                    ],
                    'doc_count_error_upper_bound': 0,
                    'sum_other_doc_count': 0
                }
            },
            'hits': {'hits': [], 'max_score': 0.0, 'total': 147},
            'timed_out': False,
            'took': 74
        }

        result = queries._compute_journals_status(query_result)

        expected = {
            'current': 89,
            'deceased': 24,
            'inprogress': 4,
            'suspended': 30,
            'total': 147
        }

        self.assertEqual(expected, result)

    def test_compute_journal_composition(self):

        query_result = {
            "aggregations": {
                "citations": {
                    "value": 80984.0
                },
                "citable": {
                    "doc_count": 4167
                },
                "issues": {
                    "value": 292
                }
            },
            "timed_out": False,
            "hits": {
                "hits": [],
                "total": 4584,
                "max_score": 0.0
            },
            "took": 223,
            "_shards": {
                "successful": 5,
                "total": 5,
                "failed": 0
            }
        }

        result = queries._compute_journal_composition(query_result)

        expected = {
            'documents': 4584,
            'issues': 292,
            'citable_documents': 4167,
            'citations': 80984
        }

        self.assertEqual(expected, result)

    def test_compute_collection_composition(self):

        query_result = {
            "hits": {
                "hits": [],
                "total": 340361,
                "max_score": 0.0
            },
            "timed_out": False,
            "aggregations": {
                "journals": {
                    "value": 357
                },
                "citations": {
                    "value": 8110770.0
                },
                "issues": {
                    "value": 21011
                },
                "citable": {
                    "doc_count": 309868
                }
            },
            "took": 224,
            "_shards": {
                "successful": 5,
                "failed": 0,
                "total": 5
            }
        }

        result = queries._compute_collection_composition(query_result)

        expected = {
            'documents': 340361,
            'issues': 21011,
            'citable_documents': 309868,
            'citations': 8110770,
            'journals': 357
        }

        self.assertEqual(expected, result)
