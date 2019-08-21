import unittest

from src.filter.conditions.grep_condition import GrepCondition
from src.filter.filter_error import FilterError
from src.network.request.requester import Requester
from test.mocks.httpserver.http_request_handler import HTTPRequestHandler
from test.mocks.httpserver.http_server_manager import HTTPServerManager
from test.mocks.utils import random_port
from test.mocks.wordlist_mock import WordlistMock


class GrepConditionTest(unittest.TestCase):
    def test_setup(self):
        condition = GrepCondition()
        with self.assertRaises(FilterError, msg='Check on invalid pattern failed'):
            condition.setup(condition_args='[')
        with self.assertRaises(FilterError, msg='Check on invalid grep part failed'):
            condition.setup(condition_args='', handler_args='test')

    def test_match(self):
        class Handler(HTTPRequestHandler):
            def do_GET(self):
                payload = b'body_grep_value'
                end = b'\r\n'
                content_length = len(payload) + len(end)
                self._set_headers(status_code=200,
                                  headers={'Content-Type': 'text/html',
                                           'Grep-Header': 'headers_grep_value',
                                           'Content-Length': content_length})
                self.wfile.write(b'%b%b' % (payload, end,))

        condition = GrepCondition()
        wordlist = iter(WordlistMock())
        with HTTPServerManager(handler=Handler, port=random_port()) as server:
            response = Requester(url=server.url).request(next(wordlist))
            condition.setup(condition_args='abc', handler_args='headers')
            self.assertFalse(condition.match(response.body), msg='Check on wrong pattern in headers failed')
            condition.setup(condition_args='headers_grep*', handler_args='headers')
            self.assertTrue(condition.match(response.body), msg='Check on right pattern in headers failed')
            condition.setup(condition_args='abc', handler_args='body')
            self.assertFalse(condition.match(response.body), msg='Check on wrong pattern in body failed')
            condition.setup(condition_args='body_grep*', handler_args='body')
            self.assertTrue(condition.match(response.body), msg='Check on right pattern in body failed')
            condition.setup(condition_args='abc')
            self.assertFalse(condition.match(response.body), msg='Check on wrong pattern in headers or body failed')
            condition.setup(condition_args='/*grep_value')
            self.assertTrue(condition.match(response.body), msg='Check on right pattern in headers or body failed')
