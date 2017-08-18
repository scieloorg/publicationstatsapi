import json
import re

from publicationstats.client import ThriftClient
from publicationstats import utils

REGEX_ISSN = re.compile("^[0-9]{4}-[0-9]{3}[0-9xX]$")
REGEX_ISSUE = re.compile("^[0-9]{4}-[0-9]{3}[0-9xX][0-2][0-9]{3}[0-9]{4}$")
REGEX_ARTICLE = re.compile("^S[0-9]{4}-[0-9]{3}[0-9xX][0-2][0-9]{3}[0-9]{4}[0-9]{5}$")


def _code_type(code):

    if not code:
        return None

    if REGEX_ISSN.match(code):
        return 'issn'

    if REGEX_ISSUE.match(code):
        return 'issue'

    if REGEX_ARTICLE.match(code):
        return 'pid'


def _compute_journal_composition(query_result):

    result = {
        'documents': int(query_result['hits']['total']),
        'citable_documents': int(query_result['aggregations']['citable']['doc_count']),
        'issues': int(query_result['aggregations']['issues']['value']),
        'citations': int(query_result['aggregations']['citations']['value'])
    }

    return result


def journal_composition(collection, issn, raw=False):
    """
    This method retrieve the total of documents, articles (citable documents),
    issues and bibliografic references of a journal

    arguments
    collection: SciELO 3 letters Acronym
    issn: Journal ISSN

    return for journal context
    {
        "citable": 12140,
        "non_citable": 20,
        "docs": 12160,
        "issues": 120,
        "references": 286619
    }
    """

    tc = ThriftClient()

    body = {"query": {"filtered": {}}}

    fltr = {}

    query = {
        "query": {
            "bool": {
                "must": [
                    {
                        "match": {
                            "collection": collection
                        }
                    },
                    {
                        "match": {
                            "issn": issn
                        }
                    },
                ]
            }
        }
    }

    body['query']['filtered'].update(fltr)
    body['query']['filtered'].update(query)

    query_parameters = [
        ('size', '0'),
        ('search_type', 'count')
    ]

    body['aggs'] = {
        "issues": {
            "cardinality": {
                "field": "issue"
            }
        },
        "citations": {
            "sum": {
                "field": "citations"
            }
        },
        "citable": {
            "filter": {
                "terms": {
                    "document_type": [i for i in utils.CITABLE_DOCUMENT_TYPES]
                }
            }
        }
    }

    query_result = tc.search('article', json.dumps(body), query_parameters)

    computed = _compute_journal_composition(query_result)

    return query_result if raw else computed


def _compute_collection_composition(query_result):

    result = {
        'documents': int(query_result['hits']['total']),
        'citable_documents': int(query_result['aggregations']['citable']['doc_count']),
        'issues': int(query_result['aggregations']['issues']['value']),
        'journals': int(query_result['aggregations']['journals']['value']),
        'citations': int(query_result['aggregations']['citations']['value'])
    }

    return result


def collection_composition(collection, raw=False):
    """
    This method retrieve the total of documents, articles (citable documents),
    issues and bibliografic references of a journal

    arguments
    collection: SciELO 3 letters Acronym
    issn: Journal ISSN

    return for journal context
    {
        "citable": 12140,
        "non_citable": 20,
        "docs": 12160,
        "issues": 120,
        "references": 286619
    }
    """

    tc = ThriftClient()

    body = {"query": {"filtered": {}}}

    fltr = {}

    query = {
        "query": {
            "bool": {
                "must": [
                    {
                        "match": {
                            "collection": collection
                        }
                    }
                ]
            }
        }
    }

    body['query']['filtered'].update(fltr)
    body['query']['filtered'].update(query)

    query_parameters = [
        ('size', '0'),
        ('search_type', 'count')
    ]

    body['aggs'] = {
        "journals": {
            "cardinality": {
                "field": "issn"
            }
        },
        "issues": {
            "cardinality": {
                "field": "issue"
            }
        },
        "citations": {
            "sum": {
                "field": "citations"
            }
        },
        "citable": {
            "filter": {
                "terms": {
                    "document_type": [i for i in utils.CITABLE_DOCUMENT_TYPES]
                }
            }
        }
    }

    query_result = tc.search('article', json.dumps(body), query_parameters)

    computed = _compute_collection_composition(query_result)

    return query_result if raw else computed


def _compute_journals_status(query_result):

    result = {
     'current': 0,
     'suspended': 0,
     'deceased': 0,
     'inprogress': 0,
     'total': 0
    }

    for item in query_result['aggregations']['status']['buckets']:
        result[item['key']] = item['doc_count']
        result['total'] += item['doc_count']

    return result


def journals_status(collection, raw=False):
    """
    This method retrieve the total of documents, articles (citable documents),
    issues and bibliografic references of a journal

    arguments
    collection: SciELO 3 letters Acronym
    issn: Journal ISSN

    return for journal context
    {
        "citable": 12140,
        "non_citable": 20,
        "docs": 12160,
        "issues": 120,
        "references": 286619
    }
    """

    tc = ThriftClient()

    body = {"query": {"filtered": {}}}

    fltr = {}

    query = {
        "query": {
            "bool": {
                "must": [
                    {
                        "match": {
                            "collection": collection
                        }
                    }
                ]
            }
        }
    }

    body['query']['filtered'].update(fltr)
    body['query']['filtered'].update(query)

    query_parameters = [
        ('size', '0'),
        ('search_type', 'count')
    ]

    body['aggs'] = {
        "status": {
            "terms": {
                "field": "status"
            }
        }
    }

    query_result = tc.search('journal', json.dumps(body), query_parameters)

    computed = _compute_journals_status(query_result)

    return query_result if raw else computed
