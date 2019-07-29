import threading


class ThreadSafeIterator:
    def __init__(self, iterator):
        self._iterator = iterator
        self._lock = threading.Lock()

    def __iter__(self):
        return self

    def __next__(self):
        with self._lock:
            return self._iterator.__next__()


def thread_safe_iterator(iterator):
    def wrap(*args, **kwargs):
        return ThreadSafeIterator(iterator(*args, **kwargs))
    return wrap
