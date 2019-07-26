import threading

from src import output
from src.network.response.ResponseType import ResponseType
from src.wordlist.Wordlist import Wordlist
from src.filter.Filter import Filter
from src.network.request.RequestError import RequestError
from src.network.request.Requester import Requester


class Fuzzer:
    def __init__(self, wordlist: Wordlist, requester: Requester, filter: Filter, threads: int = 1):
        self._wordlist = wordlist
        self._requester = requester
        self._filter = filter
        self.threads = threads
        self._wordlist_len = len(self._wordlist)
        self._is_cancel_lock = threading.Lock()
        self._is_cancel = False
        self._paths = None
        self._index_lock = threading.Lock()
        self._index = 0

    def start(self):
        threads = set()
        try:
            self._is_cancel = False
            self._paths = iter(self._wordlist)
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
                except StopIteration:
                    break
                response = self._requester.request(path=path)
                if self._canceled():
                    break
                if response.type == ResponseType.error:
                    output.error(response.body)
                else:
                    response = response.body
                    if self._filter.inspect(response):
                        output.response(response)

                output.progress_bar(float(self._index_increment()) / float(self._wordlist_len) * 100)
        except RequestError as e:
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
