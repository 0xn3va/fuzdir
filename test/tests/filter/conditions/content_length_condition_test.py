import unittest

from src.filter.conditions.content_length_condition import ContentLengthCondition
from src.filter.filter_error import FilterError
from src.network.request.requester import Requester
from test.mocks.httpserver.http_request_handler import HTTPRequestHandler
from test.mocks.httpserver.http_server_manager import HTTPServerManager
from test.mocks.utils import random_port
from test.mocks.wordlist_mock import WordlistMock


class ContentLengthConditionTest(unittest.TestCase):
    def test_setup(self):
        condition = ContentLengthCondition()
        # empty line
        with self.assertRaises(FilterError, msg='Check on setup with empty line failed'):
            condition.setup(condition_args='-')
        # incorrect length
        with self.assertRaises(FilterError, msg='Check on setup with incorrect length failed'):
            condition.setup(condition_args='-10')
        # incorrect range
        with self.assertRaises(FilterError, msg='Check on setup with incorrect range failed'):
            condition.setup(condition_args='100-10')
        # list of status codes with separator in the end of line
        condition.setup(condition_args='10-100,10,')
        self.assertListEqual(condition._ranges, [[10, 100], [10]],
                             msg='Check on setup with separator in the end line failed')

    def test_match(self):
        class Handler(HTTPRequestHandler):
            def do_GET(self):
                payload = b'a' * 14
                end = b'\r\n'
                content_length = len(payload) + len(end)
                self._set_headers(status_code=200,
                                  headers={'Content-Type': 'text/html', 'Content-Length': content_length})
                self.wfile.write(b'%b%b' % (payload, end,))

        condition = ContentLengthCondition()
        wordlist = iter(WordlistMock())
        with HTTPServerManager(handler=Handler, port=random_port()) as server:
            response = Requester(url=server.url).request(next(wordlist))
            # wrong length
            condition.setup(condition_args='0')
            self.assertFalse(condition.match(response.body), msg='Check on wrong length matching failed')
            # right length
            condition.setup(condition_args='16')
            self.assertTrue(condition.match(response.body), msg='Check on right length matching failed')
            # wrong range
            condition.setup(condition_args='0-10')
            self.assertFalse(condition.match(response.body), msg='Check on wrong range matching failed')
            # right range
            condition.setup(condition_args='0-20')
            self.assertTrue(condition.match(response.body), msg='Check on right range matching failed')
            # multiple ranges
            condition.setup(condition_args='10-18,20-30')
            self.assertTrue(condition.match(response.body), msg='Check on multiple ranges matching failed')
