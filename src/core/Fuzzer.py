import threading

from src.core.Wordlist import Wordlist
from src.filter.Filter import Filter
from src.network.RequestError import RequestError
from src.network.Requests import Requests
from src.output.Output import Output
from src.utils.Message import MessageType


class Fuzzer:
    def __init__(self, wordlist: Wordlist, requests: Requests, filter: Filter, threads: int = 1):
        self._wordlist = wordlist
        self._wordlist_len = len(self._wordlist)
        self._requests = requests
        self._filter = filter
        self.threads = threads
        self._shutdown_lock = threading.Lock()
        self._index_lock = threading.Lock()
        self._shutdown = False
        self._paths = None
        self._index = 0

    @property
    def _shutdown(self):
        with self._shutdown_lock:
            return self._cancel

    @_shutdown.setter
    def _shutdown(self, shutdown: bool):
        with self._shutdown_lock:
            self._cancel = shutdown

    def _index_increment(self):
        with self._index_lock:
            self._index += 1
            return self._index

    def _request(self, output: Output):
        try:
            while True:
                try:
                    path = next(self._paths)
                except StopIteration:
                    break
                message = self._requests.request(path=path)
                if self._shutdown:
                    break
                if message.type == MessageType.error:
                    output.print_error_log(message.body)
                else:
                    response = message.body
                    if self._filter.inspect(response):
                        output.print_response(response)

                output.print_progress_bar(float(self._index_increment()) / float(self._wordlist_len) * 100)
        except RequestError as e:
            self._shutdown = True
            output.print_error(str(e))
            return

    def start(self, output: Output):
        threads = set()
        try:
            self._shutdown = False
            self._paths = iter(self._wordlist)
            self._index = 0

            for _ in range(self.threads):
                thread = threading.Thread(target=self._request, args=(output,))
                threads.add(thread)
                thread.start()

            for thread in threads:
                thread.join()
        except KeyboardInterrupt:
            self._shutdown = True
            output.print_error('KeyboardInterrupt')
        finally:
            while any(thread.is_alive() for thread in threads):
                try:
                    for thread in threads:
                        thread.join()
                except KeyboardInterrupt:
                    continue
