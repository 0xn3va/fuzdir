import threading

import requests

from src import output
from src.dictionary.dictionary import Dictionary
from src.filter.filter import Filter
from src.network.requester.requester import Requester


class Fuzzer:
    default_threads = 10

    def __init__(self, dictionary: Dictionary, requester: Requester, filter: Filter, threads: int = default_threads):
        self._dictionary = dictionary
        self._requester = requester
        self._filter = filter
        self.threads = threads
        self._dictionary_len = len(self._dictionary)
        self._is_cancel_lock = threading.Lock()
        self._is_cancel = False
        self._paths = None
        self._index_lock = threading.Lock()
        self._index = 0

    def start(self):
        threads = set()
        try:
            self._is_cancel = False
            self._paths = iter(self._dictionary)
            self._index = 0

            for _ in range(self.threads):
                thread = threading.Thread(target=self._request)
                threads.add(thread)
                thread.start()

            for thread in threads:
                thread.join()
        except KeyboardInterrupt:
            self._cancel('User aborted')
        finally:
            while any(thread.is_alive() for thread in threads):
                try:
                    for thread in threads:
                        thread.join()
                except KeyboardInterrupt:
                    continue

    def _request(self):
        try:
            while True:
                try:
                    path = next(self._paths)
                    response = self._requester.request(path=path)
                    if self._canceled():
                        break
                    if self._filter.inspect(response):
                        output.response(response)
                    output.progress_bar(float(self._index_increment()) / float(self._dictionary_len) * 100)
                except StopIteration:
                    break
                except requests.exceptions.RetryError as e:
                    output.error(str(e))
        except requests.exceptions.TooManyRedirects as e:
            self._cancel('Too many redirects: %s' % (str(e),))
        except requests.exceptions.SSLError:
            self._cancel('SSL error connection to server')
        except requests.exceptions.ConnectionError:
            self._cancel('Failed to establish a connection with %s' % (self._requester.url,))
        except Exception as e:
            self._cancel(str(e))

    def _canceled(self):
        with self._is_cancel_lock:
            return self._is_cancel

    def _cancel(self, e: str):
        with self._is_cancel_lock:
            if not self._is_cancel:
                self._is_cancel = True
                output.error(e)

    def _index_increment(self):
        with self._index_lock:
            self._index += 1
            return self._index
