from concurrent.futures import ThreadPoolExecutor, Future, TimeoutError, CancelledError

from src.core.Wordlist import Wordlist
from src.filter.Filter import Filter
from src.network.Requests import Requests
from src.output.CLIOutput import CLIOutput
from src.utils.Message import MessageType


class Fuzzer:
    def __init__(self, wordlist: Wordlist, requests: Requests, filter: Filter, output: CLIOutput, threads: int = 1):
        self._wordlist = wordlist
        self._requests = requests
        self._filter = filter
        self._output = output
        self._max_threads = threads

    @property
    def threads(self):
        return self._max_threads

    def start(self):
        paths = iter(self._wordlist)
        task = self._requests.request
        result = Future()

        with ThreadPoolExecutor(max_workers=self._max_threads) as executor:
            def request():
                try:
                    index, path = next(paths)
                    future = executor.submit(task, index=index, path=path)
                    future.add_done_callback(request_done)
                except StopIteration:
                    result.cancel()
                    return

            def request_done(future):
                exception = future.exception()
                if exception is not None:
                    self._output.print_error(str(exception))
                    result.cancel()
                    return
                message = future.result()
                if message.type == MessageType.error:
                    # todo('Write to error log')
                    print(message.body)
                else:
                    index, response = message.body
                    self._output.progress_bar(float(index) / float(self._wordlist.size) * 100)
                    if self._filter.inspect(response):
                        self._output.print_response(response)
                if not result.cancelled():
                    request()

            for _ in range(self._max_threads):
                request()

            try:
                while not result.done():
                    try:
                        result.result(.2)
                    except (TimeoutError, CancelledError):
                        pass
            except KeyboardInterrupt:
                result.cancel()
                return
