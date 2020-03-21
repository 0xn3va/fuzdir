import unittest

from src.argument_parser.actions.condition_parser.implement.status_code_condition_parser import \
    StatusCodeConditionParser
from src.filter.condition.implement.status_code_condition import StatusCodeCondition
from src.network.requester.requester import Requester
from test import ignore_resource_warning
from test.mocks.httpserver.http_request_handler import HTTPRequestHandler
from test.mocks.httpserver.http_server_manager import HTTPServerManager
from test.mocks.utils import random_port, random_string


class StatusCodeConditionTest(unittest.TestCase):
    @ignore_resource_warning
    def test_match(self):
        class Handler(HTTPRequestHandler):
            def do_GET(self):
                self._set_headers(status_code=200, headers={'Content-Type': 'text/html', 'Content-Length': 0})

        with HTTPServerManager(handler=Handler, port=random_port()) as server:
            response = Requester(url=server.url).request(random_string())

            parser = StatusCodeConditionParser()
            condition = StatusCodeCondition(args=parser.parse_arguments('200'), area='')
            self.assertTrue(condition.match(response), msg='Check on matching of right status code failed')

            condition = StatusCodeCondition(args=parser.parse_arguments('400'), area='')
            self.assertFalse(condition.match(response), msg='Check on matching of wrong status code failed')
