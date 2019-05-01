import threading

from src.core.Wordlist import Wordlist
from src.filter.Filter import Filter
from src.network.RequestError import RequestError
from src.network.Requests import Requests
from src.output.CLIOutput import CLIOutput
from src.utils.Message import MessageType


class Fuzzer:
    def __init__(self, wordlist: Wordlist, requests: Requests, filter: Filter, output: CLIOutput, threads: int = 1):
        self._wordlist = wordlist
        self._requests = requests
        self._filter = filter
        self._output = output
        self._threads = set()
        for _ in range(threads):
            self._threads.add(threading.Thread(target=self._request))
        self._lock = threading.Lock()
        self._shutdown = False
        self.paths = None

    @property
    def threads(self):
        return len(self._threads)

    @property
    def _shutdown(self):
        with self._lock:
            return self._cancel

    @_shutdown.setter
    def _shutdown(self, shutdown: bool):
        with self._lock:
            self._cancel = shutdown

    def _request(self):
        try:
            while True:
                if self._shutdown:
                    break

                index, path = next(self.paths)
                message = self._requests.request(index=index, path=path)

                if message.type == MessageType.error:
                    # todo('Write to error log')
                    #print(message.body)
                    pass
                else:
                    index, response = message.body
                    if self._filter.inspect(response):
                        self._output.print_response(response)

                self._output.progress_bar(float(index) / float(self._wordlist.size) * 100)
        except RequestError as e:
            self._shutdown = True
            self._output.print_error(str(e))
            return
        except StopIteration:
            return

    def start(self):
        try:
            self._shutdown = False
            self.paths = iter(self._wordlist)

            for thread in self._threads:
                thread.start()

            for thread in self._threads:
                thread.join()
        except KeyboardInterrupt:
            self._output.print_error('KeyboardInterrupt')
            self._shutdown = True
            return
