import unittest

from src.filter.condition.implement.status_code_condition import StatusCodeCondition
from src.filter.filter_error import FilterError
from src.network.requester.requester import Requester
from test import ignore_resource_warning
from test.mocks.httpserver.http_request_handler import HTTPRequestHandler
from test.mocks.httpserver.http_server_manager import HTTPServerManager
from test.mocks.utils import random_port, random_string


class CodeConditionTest(unittest.TestCase):
    def test_setup(self):
        condition = StatusCodeCondition()
        # empty line
        with self.assertRaises(FilterError, msg='Check on setup with empty line failed'):
            condition.setup(args='', area='')
        # not numbers
        with self.assertRaises(FilterError, msg='Check on setup with non number failed'):
            condition.setup(args='a,a', area='')
        # incorrect status code
        with self.assertRaises(FilterError, msg='Check on setup with incorrect status code failed'):
            condition.setup(args='0', area='')
        # list of status codes with separator in the end of line
        condition.setup(args='200,404,', area='')
        self.assertListEqual(condition._codes, [(200, 200), (404, 404)],
                             msg='Check on setup with separator in the end line failed')

    @ignore_resource_warning
    def test_match(self):
        class Handler(HTTPRequestHandler):
            def do_GET(self):
                self._set_headers(status_code=200, headers={'Content-Type': 'text/html', 'Content-Length': 0})

        condition = StatusCodeCondition()
        with HTTPServerManager(handler=Handler, port=random_port()) as server:
            response = Requester(url=server.url).request(random_string())
            condition.setup(args='200', area='')
            self.assertTrue(condition.match(response), msg='Check on matching of right status code failed')
            condition.setup(args='400', area='')
            self.assertFalse(condition.match(response), msg='Check on matching of wrong status code failed')
