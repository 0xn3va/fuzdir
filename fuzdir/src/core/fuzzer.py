import logging
import threading
from queue import Empty

import requests

from src.output import progress_bar as print_progress_bar, error as print_error, response as print_response
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
            dictionary = self._dictionary
            request = self._requester.request
            canceled = self._canceled
            inspect = self._filter.inspect
            index_increment = self._index_increment
            delta = 1 / self._dictionary_len * 100

            while True:
                try:
                    sample = dictionary.get()
                    response = request(path=sample)
                    if canceled():
                        break
                    if inspect(response):
                        print_response(response)
                    print_progress_bar(index_increment() * delta)
                except Empty:
                    break
        except requests.exceptions.TooManyRedirects as e:
            self._cancel(f'Too many redirects: {str(e)}')
        except requests.exceptions.SSLError:
            self._cancel('SSL error connection to server')
        except requests.exceptions.ConnectionError:
            self._cancel(f'Failed to establish a connection with {self._requester.url}')
        except requests.exceptions.RetryError as e:
            self._cancel(f'Max retries exceeded with url: {e.request.path_url}')
        except Exception as e:
            self._cancel(str(e))

    def _canceled(self):
        with self._is_cancel_lock:
            return self._is_cancel

    def _cancel(self, e: str):
        with self._is_cancel_lock:
            if not self._is_cancel:
                logging.debug(f'Fuzzing failed, an error has occurred: {e}')
                print_error(e)
                self._is_cancel = True
                self._dictionary.cancel()

    def _index_increment(self):
        with self._index_lock:
            index = self._index + 1
            self._index = index
            return index
