import unittest

from src.filter.condition.implement.grep_condition import GrepCondition
from src.filter.filter_error import FilterError
from src.network.requester.requester import Requester
from test.mocks.httpserver.http_request_handler import HTTPRequestHandler
from test.mocks.httpserver.http_server_manager import HTTPServerManager
from test.mocks.utils import random_port, random_string


class GrepConditionTest(unittest.TestCase):
    def test_setup(self):
        condition = GrepCondition()
        with self.assertRaises(FilterError, msg='Check on invalid pattern failed'):
            condition.setup(args='[', area='')
        with self.assertRaises(FilterError, msg='Check on invalid grep part failed'):
            condition.setup(args='', area='test')

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
        with HTTPServerManager(handler=Handler, port=random_port()) as server:
            response = Requester(url=server.url).request(random_string())
            condition.setup(args='abc', area='headers')
            self.assertFalse(condition.match(response), msg='Check on wrong pattern in headers failed')
            condition.setup(args='headers_grep*', area='headers')
            self.assertTrue(condition.match(response), msg='Check on right pattern in headers failed')
            condition.setup(args='abc', area='body')
            self.assertFalse(condition.match(response), msg='Check on wrong pattern in body failed')
            condition.setup(args='body_grep*', area='body')
            self.assertTrue(condition.match(response), msg='Check on right pattern in body failed')
            condition.setup(args='abc', area='')
            self.assertFalse(condition.match(response), msg='Check on wrong pattern in headers or body failed')
            condition.setup(args='/*grep_value', area='')
            self.assertTrue(condition.match(response), msg='Check on right pattern in headers or body failed')
