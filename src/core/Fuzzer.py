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
        self._lock = threading.Lock()
        self._shutdown = False
        self._paths = None
        self._index = 0

    @property
    def _shutdown(self):
        with self._lock:
            return self._cancel

    @_shutdown.setter
    def _shutdown(self, shutdown: bool):
        with self._lock:
            self._cancel = shutdown

    def _request(self, output: Output):
        try:
            while True:
                if self._shutdown:
                    break

                path = next(self._paths)
                message = self._requests.request(path=path)

                if message.type == MessageType.error:
                    output.print_error_log(message.body)
                else:
                    response = message.body
                    if self._filter.inspect(response):
                        output.print_response(response)

                with self._lock:
                    self._index += 1
                    output.print_progress_bar(float(self._index) / float(self._wordlist_len) * 100)
        except RequestError as e:
            self._shutdown = True
            output.print_error(str(e))
            return
        except StopIteration:
            return

    def start(self, output: Output):
        try:
            self._shutdown = False
            self._paths = iter(self._wordlist)
            self._index = 0

            threads = set()
            for _ in range(self.threads):
                thread = threading.Thread(target=self._request, args=(output,))
                threads.add(thread)
                thread.start()

            for thread in threads:
                thread.join()
        except KeyboardInterrupt:
            output.print_error('KeyboardInterrupt')
            self._shutdown = True
            return
