import random
import time
import unittest

import requests
import urllib3

from src.network.requester.requester_error import RequesterError
from src.network.requester.requester import Requester
from src.network.requester.throttle.confidence_interval import ConfidenceInterval
from src.utils.singleton import Singleton

from test import ignore_resource_warning
from test.mocks.httpserver.http_request_handler import HTTPRequestHandler
from test.mocks.httpserver.http_server_manager import HTTPServerManager
from test.mocks.utils import random_port, random_string


class RequesterTest(unittest.TestCase):
    _stable_iterations = 2 * ConfidenceInterval._window_size
    _changeable_iterations = 4 * ConfidenceInterval._window_size
    _delta = 0.05

    def test_urls(self):
        http_scheme = 'http'
        file_scheme = 'file'
        hostname = 'localhost'
        # scheme and port by default
        requester = Requester(url=hostname)
        self.assertEqual(requester.url, '%s://%s/' % (http_scheme, hostname,),
                         msg='Check for setting scheme and port by default failed')
        # unknown scheme
        with self.assertRaises(RequesterError, msg='Check for unknown scheme failed'):
            Requester(url='%s://%s' % (file_scheme, hostname,))
        # incorrect hostname
        with self.assertRaises(RequesterError, msg='Check for incorrect hostname failed'):
            Requester(url='%s://%s' % (http_scheme, '',))
        # custom port
        custom_port_url = '%s://%s:%d/' % (http_scheme, hostname, random_port(),)
        requester = Requester(url=custom_port_url)
        self.assertEqual(requester.url, custom_port_url, msg='Check for setting custom port failed')
        # non-root path
        path = '%s/%s' % (random_string(), random_string(),)
        requester = Requester(url='%s://%s/%s' % (http_scheme, hostname, path,))
        self.assertEqual(requester.url, '%s://%s/%s/' % (http_scheme, hostname, path,),
                         msg='Check for fuzzing by non-root path failed')

    @ignore_resource_warning
    def test_retry(self):
        class Handler(HTTPRequestHandler):
            def do_GET(self):
                self._set_headers(status_code=502, headers={'Content-Type': 'text/html', 'Content-Length': 0})

        with HTTPServerManager(handler=Handler, port=random_port()) as server:
            with self.assertRaises(requests.exceptions.RetryError,  msg='Check a max retries exceeded failed'):
                _ = Requester(url=server.url).request(random_string())

            try:
                _ = Requester(url=server.url, raise_on_status=False).request(random_string())
            except requests.exceptions.RetryError:
                self.fail(msg='Check an ignoring fail of retry requests')

    @ignore_resource_warning
    def test_proxy(self):
        class Handler(HTTPRequestHandler):
            pass

        with HTTPServerManager(handler=Handler, port=random_port()) as server:
            with self.assertRaises(requests.exceptions.InvalidProxyURL, msg='Check on invalid proxy url failed'):
                requester = Requester(url=server.url, proxy='tcp://')
                _ = requester.request(random_string())

            with self.assertRaises(urllib3.exceptions.ProxySchemeUnknown,
                                   msg='Check on not supported proxy scheme failed'):
                requester = Requester(url=server.url, proxy='tcp://localhost')
                _ = requester.request(random_string())

            with self.assertRaises(requests.exceptions.ConnectionError, msg='Check on connection refused failed'):
                requester = Requester(url=server.url, proxy='socks5://localhost:%d' % (random_port(),))
                _ = requester.request(random_string())

    @ignore_resource_warning
    def test_throttle_fixed(self):
        class Handler(HTTPRequestHandler):
            pass

        throttling_period = random.uniform(0., 0.25)
        with HTTPServerManager(handler=Handler, port=random_port()) as server:
            requester = Requester(url=server.url, throttling_period=throttling_period)
            prev_time = None
            for _ in range(self._stable_iterations):
                _ = requester.request(random_string())
                current_time = time.time()
                if prev_time is not None:
                    self.assertLess(abs(throttling_period - (current_time - prev_time)), self._delta,
                                    msg='Check on fixed throttling period failed')
                prev_time = current_time

    @ignore_resource_warning
    def test_throttle_dynamic(self):
        class Handler(HTTPRequestHandler, metaclass=Singleton):
            delta = 0.001
            delay = 0.
            fixed_iterations = self._stable_iterations
            increasing_iterations = fixed_iterations + self._changeable_iterations
            decreasing_iterations = increasing_iterations + self._changeable_iterations
            i = 0

            def do_GET(self):
                self._set_headers(status_code=200, headers={'Content-Type': 'text/html', 'Content-Length': 0})
                if self.fixed_iterations <= self.i < self.increasing_iterations:
                    self.delay += self.delta
                elif self.increasing_iterations <= self.i < self.decreasing_iterations:
                    self.delay -= self.delta
                    if self.delay < 0:
                        self.delay = 0.
                self.i += 1
                time.sleep(self.delay)

        with HTTPServerManager(handler=Handler, port=random_port()) as server:
            requester = Requester(url=server.url)
            period = None
            # stable
            for _ in range(self._stable_iterations):
                _ = requester.request(random_string())
                period = requester._throttle._interval._period
                self.assertEqual(period, 0., msg='Check for no delay failed')
            # increase
            is_changed = False
            for _ in range(self._changeable_iterations):
                _ = requester.request(random_string())
                p = requester._throttle._interval._period
                if p != period:
                    is_changed = True
                    self.assertLess(period, p, msg='Check for increasing delay failed')
                    period = p
            self.assertTrue(is_changed, msg='Check for increasing delay failed')
            # decreasing
            is_changed = False
            for i in range(self._changeable_iterations):
                _ = requester.request(random_string())
                p = requester._throttle._interval._period
                if p != period:
                    if is_changed:
                        self.assertGreater(period, p, msg='Check for decreasing delay failed')
                    is_changed = True
                    period = p
            self.assertTrue(is_changed, msg='Check for decreasing delay failed')
            # stable
            for _ in range(self._stable_iterations):
                _ = requester.request(random_string())
                period = requester._throttle._interval._period
            self.assertEqual(period, 0., msg='Check to return to initial state failed')
