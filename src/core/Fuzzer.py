import threading

from src.network.response.ResponseType import ResponseType
from src.wordlist.Wordlist import Wordlist
from src.filter.Filter import Filter
from src.network.request.RequestError import RequestError
from src.network.request.Requester import Requester
from src.output.MessageType import MessageType
from src.output.Output import Output


class Fuzzer:
    def __init__(self, wordlist: Wordlist, requester: Requester, filter: Filter, threads: int = 1):
        self._wordlist = wordlist
        self._wordlist_len = len(self._wordlist)
        self._requester = requester
        self._filter = filter
        self.threads = threads
        self._is_cancel_lock = threading.Lock()
        self._index_lock = threading.Lock()
        self._is_cancel = False
        self._paths = None
        self._index = 0

    @property
    def _is_cancel(self):
        with self._is_cancel_lock:
            return self._status

    @_is_cancel.setter
    def _is_cancel(self, status: bool):
        with self._is_cancel_lock:
            self._status = status

    def start(self, output: Output):
        threads = set()
        try:
            self._is_cancel = False
            self._paths = iter(self._wordlist)
            self._index = 0

            for _ in range(self.threads):
                thread = threading.Thread(target=self._request, args=(output,))
                threads.add(thread)
                thread.start()

            for thread in threads:
                thread.join()
        except KeyboardInterrupt:
            self._cancel(output, 'KeyboardInterrupt')
        finally:
            while any(thread.is_alive() for thread in threads):
                try:
                    for thread in threads:
                        thread.join()
                except KeyboardInterrupt:
                    continue

    def _request(self, output: Output):
        try:
            while True:
                try:
                    path = next(self._paths)
                except StopIteration:
                    break
                message = self._requester.request(path=path)
                if self._canceled():
                    break
                if message.type == ResponseType.error:
                    output.print(MessageType.log, message.body)
                else:
                    response = message.body
                    if self._filter.inspect(response):
                        output.print_response(response)

                # output.progress_bar(float(self._index_increment()) / float(self._wordlist_len) * 100)
        except RequestError as e:
            self._cancel(output, str(e))

    def _canceled(self):
        return self._is_cancel

    def _cancel(self, output: Output, e: str):
        if not self._canceled():
            self._is_cancel = True
            output.print(MessageType.error, e)

    def _index_increment(self):
        with self._index_lock:
            self._index += 1
            return self._index
