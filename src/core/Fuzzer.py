from concurrent.futures import ThreadPoolExecutor

from src.core.Wordlist import Wordlist
from src.network.Requests import Requests


class Fuzzer:
    def __init__(self, wordlist: Wordlist, threads: int = 1):
        self._wordlist = iter(wordlist)
        self._threads = threads
        self._requester = Requests(url='127.0.0.1/test')

    def start(self):
        with ThreadPoolExecutor(max_workers=self._threads) as executor:
            executor.submit(self.thread_fn)

    def thread_fn(self):
        try:
            sample = next(self._wordlist)
            while True:
                self._requester.request(path=sample)
                sample = next(self._wordlist)
        except StopIteration:
            print('StopIteration')
            return


