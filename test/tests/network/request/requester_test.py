import random
import threading
import time
import unittest

from requests.exceptions import RetryError

from src.network.request.request_error import RequestError
from src.network.request.requester import Requester
from src.network.request.throttle.confidence_interval import ConfidenceInterval
from src.network.response.response_type import ResponseType
from src.utils.singleton import Singleton
from test.mocks.httpserver.http_request_handler import HTTPRequestHandler
from test.mocks.httpserver.http_server_manager import HTTPServerManager
from test.mocks.utils import random_port
from test.mocks.wordlist_mock import WordlistMock


class RequesterTest(unittest.TestCase):
    _wordlist = iter(WordlistMock())
    _stable_iterations = 2 * ConfidenceInterval._window_size
    _changeable_iterations = 4 * ConfidenceInterval._window_size
    _delta = 0.05

    def test_urls(self):
        http_scheme = 'http'
        file_scheme = 'file'
        hostname = 'localhost'
        port = 80
        full_url_format = '%s://%s:%d/'
        # scheme and port by default
        requester = Requester(url=hostname)
        self.assertEqual(requester.url, full_url_format % (http_scheme, hostname, port,),
                         msg='Check for setting scheme and port by default failed')
        # unknown scheme
        with self.assertRaises(RequestError, msg='Check for unknown scheme failed'):
            Requester(url='%s://%s' % (file_scheme, hostname,))
        # incorrect hostname
        with self.assertRaises(RequestError, msg='Check for incorrect hostname failed'):
            Requester(url='%s://%s' % (http_scheme, '',))
        # custom port
        custom_port_url = full_url_format % (http_scheme, hostname, random_port(),)
        requester = Requester(url=custom_port_url)
        self.assertEqual(requester.url, custom_port_url, msg='Check for setting custom port failed')
        # non-root path
        path = '%s/%s' % (next(self._wordlist), next(self._wordlist),)
        requester = Requester(url='%s://%s/%s' % (http_scheme, hostname, path,))
        self.assertEqual(requester.url, '%s://%s:%d/%s/' % (http_scheme, hostname, port, path,),
                         msg='Check for fuzzing by non-root path failed')

    def test_retry(self):
        class Handler(HTTPRequestHandler):
            def do_GET(self):
                self._set_headers(status_code=500, headers={'Content-Type': 'text/html', 'Content-Length': 0})

        with HTTPServerManager(handler=Handler, port=random_port()) as server:
            response = Requester(url=server.url).request(next(self._wordlist))
            self.assertEqual(response.type, ResponseType.error, msg='Check a retry response type failed')
            self.assertIsInstance(response.body, RetryError, msg='Check a retry response body failed')

    def test_proxy(self):
        class Handler(HTTPRequestHandler):
            pass

        with HTTPServerManager(handler=Handler, port=random_port()) as server:
            def assert_raises(proxy, msg):
                with self.assertRaises(RequestError, msg=msg):
                    requester = Requester(url=server.url, proxy=proxy)
                    _ = requester.request(next(self._wordlist))

            assert_raises(proxy='tcp://', msg='Check on invalid proxy url failed')
            assert_raises(proxy='tcp://localhost', msg='Check on not supported proxy scheme failed')
            assert_raises(proxy='socks5://localhost:%d' % (random_port(),),
                          msg='Check on connection refused failed')

    def test_throttle_fixed(self):
        class Handler(HTTPRequestHandler):
            pass

        throttling_period = random.random()
        with HTTPServerManager(handler=Handler, port=random_port()) as server:
            requester = Requester(url=server.url, throttling_period=throttling_period)
            prev_time = None
            for _ in range(self._stable_iterations):
                _ = requester.request(next(self._wordlist))
                current_time = time.time()
                if prev_time is not None:
                    self.assertLess(abs(throttling_period - (current_time - prev_time)), self._delta,
                                    msg='Check on fixed throttling period failed')
                prev_time = current_time

    def test_throttle_dynamic(self):
        class Handler(HTTPRequestHandler, metaclass=Singleton):
            delta = 0.001
            lock = threading.Lock()
            delay = 0.
            fixed_iterations = self._stable_iterations
            increasing_iterations = fixed_iterations + self._changeable_iterations
            decreasing_iterations = increasing_iterations + self._changeable_iterations
            i = 0

            def do_GET(self):
                self._set_headers(status_code=200, headers={'Content-Type': 'text/html', 'Content-Length': 0})
                with self.lock:
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
                _ = requester.request(next(self._wordlist))
                period = requester._throttle._interval._period
                self.assertEqual(period, 0., msg='Check for no delay failed')
            # increase
            is_changed = False
            for _ in range(self._changeable_iterations):
                _ = requester.request(next(self._wordlist))
                p = requester._throttle._interval._period
                if p != period:
                    is_changed = True
                    self.assertLess(period, p, msg='Check for increasing delay failed')
                    period = p
            self.assertTrue(is_changed, msg='Check for increasing delay failed')
            # decreasing
            is_changed = False
            for _ in range(self._changeable_iterations):
                _ = requester.request(next(self._wordlist))
                p = requester._throttle._interval._period
                if p != period:
                    is_changed = True
                    self.assertGreater(period, p, msg='Check for decreasing delay failed')
                    period = p
            self.assertTrue(is_changed, msg='Check for decreasing delay failed')
            # stable
            for _ in range(self._stable_iterations):
                _ = requester.request(next(self._wordlist))
                period = requester._throttle._interval._period
            self.assertEqual(period, 0., msg='Check to return to initial state failed')
