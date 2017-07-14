# coding: utf-8

import os
import thriftpy
import json
import logging
import time

# URLJOIN Python 3 and 2 import compatibilities
try:
    from urllib.parse import urljoin
except:
    from urlparse import urljoin

from thriftpy.rpc import make_client

logger = logging.getLogger(__name__)


class PublicationStatsExceptions(Exception):
    pass


class ServerError(PublicationStatsExceptions):
    pass


class ThriftClient(object):
    PUBLICATIONSTATS_THRIFT = thriftpy.load(
        os.path.join(os.path.dirname(__file__))+'/thrift/publication_stats.thrift')

    def __init__(self, domain=None):
        """
        Cliente thrift para o Articlemeta.
        """
        self.domain = domain or 'publication.scielo.org:11620'
        self._set_address()

    def _set_address(self):

        address = self.domain.split(':')

        self._address = address[0]
        try:
            self._port = int(address[1])
        except:
            self._port = 11660

    @property
    def client(self):

        client = make_client(
            self.PUBLICATIONSTATS_THRIFT.PublicationStats,
            self._address,
            self._port
        )

        return client

    def document(self, code, collection=None):
        result = self.client.document(code=code, collection=collection)

        try:
            return json.loads(result)
        except:
            return None

    def search(self, index, dsl, params):
        """
        Free queries to ES index.

        dsl (string): with DSL query
        params (list): [(key, value), (key, value)]
            where key is a query parameter, and value is the value required for
            parameter, ex: [('size', '0'), ('search_type', 'count')]
        """

        query_parameters = []

        for key, value in params:
            query_parameters.append(
                self.PUBLICATIONSTATS_THRIFT.kwargs(str(key), str(value))
            )

        try:
            result = self.client.search(index, dsl, query_parameters)
        except self.PUBLICATIONSTATS_THRIFT.ServerError:
            raise ServerError('you may trying to run a bad DSL Query')

        try:
            return json.loads(result)
        except:
            return None
