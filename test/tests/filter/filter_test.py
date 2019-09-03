import unittest

from src.filter.filter import Filter
from src.filter.filter_error import FilterError
from src.network.requester.requester import Requester

from test import ignore_resource_warning
from test.mocks.httpserver.http_request_handler import HTTPRequestHandler
from test.mocks.httpserver.http_server_manager import HTTPServerManager
from test.mocks.utils import random_port, random_string


class FilterTest(unittest.TestCase):
    def test_init(self):
        with self.assertRaises(FilterError, msg='Check on empty args failed'):
            _ = Filter(conditions='condition=')
        with self.assertRaises(FilterError, msg='Check on prefix for ignoring failed'):
            _ = Filter(conditions='not_ignore:condition=args')
        with self.assertRaises(FilterError, msg='Check on incorrect condition name failed'):
            _ = Filter(conditions='condition=args')
        with self.assertRaises(FilterError, msg='Check on incorrect arguments for condition setup failed'):
            _ = Filter(conditions='code=0')
        with self.assertRaises(FilterError, msg='Check on incorrect mode for condition setup failed'):
            _ = Filter(conditions='grep:area=args')
        filter = Filter(conditions='grep:body=args;code=400;length=10;')
        for c1, c2 in zip(filter._conditions[:-1], filter._conditions[1:]):
            _, c1 = c1
            _, c2 = c2
            self.assertGreater(c1.priority.value, c2.priority.value,
                               msg='Check on condition sorting by priority failed')

    @ignore_resource_warning
    def test_inspect(self):
        class Handler(HTTPRequestHandler):
            def do_GET(self):
                self._set_headers(status_code=200, headers={'Content-Type': 'text/html', 'Content-Length': 0})

        with HTTPServerManager(handler=Handler, port=random_port()) as server:
            response = Requester(url=server.url).request(random_string())
            filter = Filter(conditions='code=200')
            self.assertTrue(filter.inspect(response), msg='Check on right inspection failed')
            filter = Filter(conditions='code=400')
            self.assertFalse(filter.inspect(response), msg='Check on wrong inspection failed')
            filter = Filter(conditions='ignore:code=200')
            self.assertFalse(filter.inspect(response), msg='Check on wrong inspection with ignoring failed')
            filter = Filter(conditions='ignore:code=400')
            self.assertTrue(filter.inspect(response), msg='Check on right inspection with ignoring failed')
