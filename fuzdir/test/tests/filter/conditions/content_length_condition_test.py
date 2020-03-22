import unittest

from src.argument_parser.actions.parsers.condition.implement.content_length_condition_parser import \
    ContentLengthConditionParser
from src.filter.condition.implement.content_length_condition import ContentLengthCondition
from src.network.requester.requester import Requester
from test import ignore_resource_warning
from test.mocks.httpserver.http_request_handler import HTTPRequestHandler
from test.mocks.httpserver.http_server_manager import HTTPServerManager
from test.mocks.utils import random_port, random_string


class ContentLengthConditionTest(unittest.TestCase):
    @ignore_resource_warning
    def test_match(self):
        class Handler(HTTPRequestHandler):
            def do_GET(self):
                payload = b'a' * 14
                end = b'\r\n'
                content_length = len(payload) + len(end)
                self._set_headers(status_code=200,
                                  headers={'Content-Type': 'text/html', 'Content-Length': content_length})
                self.wfile.write(b'%b%b' % (payload, end,))

        with HTTPServerManager(handler=Handler, port=random_port()) as server:
            response = Requester(url=server.url).request(random_string())

            parser = ContentLengthConditionParser()
            condition = ContentLengthCondition(args=parser.parse_arguments('0'), area='')
            self.assertFalse(condition.match(response), msg='Check on wrong length matching failed')

            condition = ContentLengthCondition(args=parser.parse_arguments('16'), area='')
            self.assertTrue(condition.match(response), msg='Check on right length matching failed')

            condition = ContentLengthCondition(args=parser.parse_arguments('0-10'), area='')
            self.assertFalse(condition.match(response), msg='Check on wrong range matching failed')

            condition = ContentLengthCondition(args=parser.parse_arguments('0-20'), area='')
            self.assertTrue(condition.match(response), msg='Check on right range matching failed')

            condition = ContentLengthCondition(args=parser.parse_arguments('10-18,20-30'), area='')
            self.assertTrue(condition.match(response), msg='Check on multiple ranges matching failed')
