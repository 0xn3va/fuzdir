import unittest

from src.filter.condition.implement.content_length_condition import ContentLengthCondition
from src.filter.filter_error import FilterError
from src.network.request.requester import Requester
from test.mocks.httpserver.http_request_handler import HTTPRequestHandler
from test.mocks.httpserver.http_server_manager import HTTPServerManager
from test.mocks.utils import random_port, random_string


class ContentLengthConditionTest(unittest.TestCase):
    def test_setup(self):
        condition = ContentLengthCondition()
        # empty line
        with self.assertRaises(FilterError, msg='Check on setup with empty line failed'):
            condition.setup(args='-', area='')
        # incorrect length
        with self.assertRaises(FilterError, msg='Check on setup with incorrect length failed'):
            condition.setup(args='-10', area='')
        # incorrect range
        with self.assertRaises(FilterError, msg='Check on setup with incorrect range failed'):
            condition.setup(args='100-10', area='')
        # list of status codes with separator in the end of line
        condition.setup(args='10-100,10,', area='')
        self.assertListEqual(condition._ranges, [(10, 100), (10, 10)],
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
        with HTTPServerManager(handler=Handler, port=random_port()) as server:
            response = Requester(url=server.url).request(random_string())
            # wrong length
            condition.setup(args='0', area='')
            self.assertFalse(condition.match(response), msg='Check on wrong length matching failed')
            # right length
            condition.setup(args='16', area='')
            self.assertTrue(condition.match(response), msg='Check on right length matching failed')
            # wrong range
            condition.setup(args='0-10', area='')
            self.assertFalse(condition.match(response), msg='Check on wrong range matching failed')
            # right range
            condition.setup(args='0-20', area='')
            self.assertTrue(condition.match(response), msg='Check on right range matching failed')
            # multiple ranges
            condition.setup(args='10-18,20-30', area='')
            self.assertTrue(condition.match(response), msg='Check on multiple ranges matching failed')
