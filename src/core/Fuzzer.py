from concurrent.futures import ThreadPoolExecutor, Future, TimeoutError

from src.core.Wordlist import Wordlist
from src.filter.Filter import Filter
from src.network.Requests import Requests
from src.output.CLIOutput import CLIOutput


class Fuzzer:
    def __init__(self, wordlist: Wordlist, requests: Requests, filter: Filter, output: CLIOutput, threads: int = 1):
        self._wordlist = wordlist
        self._requests = requests
        self._filter = filter
        self._output = output
        self._max_threads = threads

    def start(self):
        paths = iter(self._wordlist)
        task = self._requests.request
        result = Future()

        executor = ThreadPoolExecutor(max_workers=self._max_threads)

        def cleanup(_):
            executor.shutdown(wait=False)

        result.add_done_callback(cleanup)

        def request():
            try:
                path = next(paths)
                if result.cancelled():
                    result.set_result('Cancel')
                    return
                future = executor.submit(task, path=path)
                future.add_done_callback(request_done)
            except StopIteration:
                result.set_result('End')
                return

        def request_done(future):
            response = future.result
            if self._filter.inspect(response):
                self._output.print_response(response)
            request()

        for _ in range(self._max_threads):
            request()

        try:
            while not result.done():
                try:
                    result.result(.2)
                except TimeoutError:
                    pass
        except KeyboardInterrupt:
            result.cancel()
            raise
