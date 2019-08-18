import random
import string

from src.wordlist.thread_safe_iterator import thread_safe_iterator


class WordlistMock:
    @thread_safe_iterator
    def __iter__(self):
        while True:
            yield ''.join(random.choices(string.ascii_lowercase, k=5))
