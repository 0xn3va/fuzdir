import unittest

from src.argument_parser.argument_manager import ArgumentManager
from src.filter.filter import Filter
from src.network.requester.requester import Requester

from test import ignore_resource_warning
from test.mocks.httpserver.http_request_handler import HTTPRequestHandler
from test.mocks.httpserver.http_server_manager import HTTPServerManager
from test.mocks.utils import random_port, random_string


class FilterTest(unittest.TestCase):
    def test_init(self):
        argument_manager = ArgumentManager()
        argument_manager.parse_args(['-u http://localhost', '-w a', '-x grep:body=args;code=400;length=10;'])
        filter = Filter(conditions=argument_manager.conditions)
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
            argument_manager = ArgumentManager()
            argument_manager.parse_args(['-u http://localhost', '-w a', '-x code=200'])
            filter = Filter(conditions=argument_manager.conditions)
            self.assertTrue(filter.inspect(response), msg='Check on right inspection failed')

            argument_manager.parse_args(['-u http://localhost', '-w a', '-x code=400'])
            filter = Filter(conditions=argument_manager.conditions)
            self.assertFalse(filter.inspect(response), msg='Check on wrong inspection failed')

            argument_manager.parse_args(['-u http://localhost', '-w a', '-x ignore:code=200'])
            filter = Filter(conditions=argument_manager.conditions)
            self.assertFalse(filter.inspect(response), msg='Check on wrong inspection with ignoring failed')

            argument_manager.parse_args(['-u http://localhost', '-w a', '-x ignore:code=400'])
            filter = Filter(conditions=argument_manager.conditions)
            self.assertTrue(filter.inspect(response), msg='Check on right inspection with ignoring failed')
