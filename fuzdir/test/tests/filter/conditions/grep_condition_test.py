import unittest

from src.argument_parser.actions.parsers.condition.implement.grep_condition_parser import GrepConditionParser
from src.filter.condition.implement.grep_condition import GrepCondition
from src.network.requester.requester import Requester
from test import ignore_resource_warning
from test.mocks.httpserver.http_request_handler import HTTPRequestHandler
from test.mocks.httpserver.http_server_manager import HTTPServerManager
from test.mocks.utils import random_port, random_string


class GrepConditionTest(unittest.TestCase):
    @ignore_resource_warning
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

        with HTTPServerManager(handler=Handler, port=random_port()) as server:
            response = Requester(url=server.url).request(random_string())

            parser = GrepConditionParser()
            condition = GrepCondition(args=parser.parse_arguments('abc'), area='headers')
            self.assertFalse(condition.match(response), msg='Check on wrong pattern in headers failed')

            condition = GrepCondition(args=parser.parse_arguments('headers_grep*'), area='headers')
            self.assertTrue(condition.match(response), msg='Check on right pattern in headers failed')

            condition = GrepCondition(args=parser.parse_arguments('abc'), area='body')
            self.assertFalse(condition.match(response), msg='Check on wrong pattern in body failed')

            condition = GrepCondition(args=parser.parse_arguments('body_grep*'), area='body')
            self.assertTrue(condition.match(response), msg='Check on right pattern in body failed')

            condition = GrepCondition(args=parser.parse_arguments('abc'), area='')
            self.assertFalse(condition.match(response), msg='Check on wrong pattern in headers or body failed')

            condition = GrepCondition(args=parser.parse_arguments('/*grep_value'), area='')
            self.assertTrue(condition.match(response), msg='Check on right pattern in headers or body failed')
