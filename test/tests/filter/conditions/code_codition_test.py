import unittest

from src.filter.conditions.code_condition import CodeCondition
from src.filter.filter_error import FilterError
from src.network.request.requester import Requester
from test.mocks.httpserver.http_request_handler import HTTPRequestHandler
from test.mocks.httpserver.http_server_manager import HTTPServerManager
from test.mocks.utils import random_port
from test.mocks.wordlist_mock import WordlistMock


class CodeConditionTest(unittest.TestCase):
    def test_setup(self):
        condition = CodeCondition()
        # empty line
        with self.assertRaises(FilterError, msg='Check on setup with empty line failed'):
            condition.setup(condition_args='')
        # not numbers
        with self.assertRaises(FilterError, msg='Check on setup with non number failed'):
            condition.setup(condition_args='a,a')
        # incorrect status code
        with self.assertRaises(FilterError, msg='Check on setup with incorrect status code failed'):
            condition.setup(condition_args='0')
        # list of status codes with separator in the end of line
        condition.setup(condition_args='200,404,')
        self.assertListEqual(condition._codes, [200, 404], msg='Check on setup with separator in the end line failed')

    def test_match(self):
        class Handler(HTTPRequestHandler):
            def do_GET(self):
                self._set_headers(status_code=200, headers={'Content-Type': 'text/html', 'Content-Length': 0})

        condition = CodeCondition()
        wordlist = iter(WordlistMock())
        with HTTPServerManager(handler=Handler, port=random_port()) as server:
            response = Requester(url=server.url).request(next(wordlist))
            condition.setup(condition_args='200')
            self.assertTrue(condition.match(response.body), msg='Check on matching of right status code failed')
            condition.setup(condition_args='400')
            self.assertFalse(condition.match(response.body), msg='Check on matching of wrong status code failed')
