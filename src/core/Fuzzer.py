from concurrent.futures import ThreadPoolExecutor, Future, TimeoutError

from src.core.Wordlist import Wordlist
from src.network.Requests import Requests


class Fuzzer:
    def __init__(self, wordlist: Wordlist, requests: Requests, threads: int = 1):
        self._wordlist = wordlist
        self._max_threads = threads
        self._requests = requests

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
            # todo('analyze future.result : request result')
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
