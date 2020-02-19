import threading
from queue import Queue, Empty

from src.dictionary.extension_list import ExtensionList
from src.dictionary.word_list import WordList


class Dictionary:
    _batches_maxsize = 2
    _samples_maxsize = 10000

    def __init__(self, word_list: WordList, extension_list: ExtensionList):
        self._word_list_iter = iter(word_list)
        self._extension_list = extension_list
        self._length = len(word_list) * (1 + len(extension_list))
        self._cancel_lock = threading.Lock()
        self._get_lock = threading.Lock()

        self._batches = Queue(maxsize=self._batches_maxsize)
        self._samples = None
        self._cancelled = False

        self._thread = threading.Thread(target=self._appending)
        self._thread.start()

    def get(self):
        with self._get_lock:
            try:
                return self._samples.get_nowait()
            except (AttributeError, Empty):
                pass

            try:
                self._samples = self._batches.get_nowait()
            except Empty:
                while True:
                    if self._cancelled:
                        self._thread.join()
                        self._samples = self._batches.get_nowait()
                    else:
                        try:
                            self._samples = self._batches.get(timeout=0.5)
                        except Empty:
                            continue
                    break

            return self._samples.get_nowait()

    def cancel(self):
        with self._cancel_lock:
            self._cancelled = True

        while self._thread.is_alive():
            try:
                self._thread.join()
            except KeyboardInterrupt:
                continue

    def _appending(self):
        word_list_iter = self._word_list_iter
        extension_list = self._extension_list
        has_pattern = extension_list.has_pattern
        pattern_symbol = extension_list.pattern_symbol
        queue = Queue()
        samples_maxsize = self._samples_maxsize

        while True:
            if self._cancelled:
                return

            try:
                word = next(word_list_iter)
            except StopIteration:
                with self._cancel_lock:
                    self._cancelled = True
                if queue.qsize() > 0:
                    self._batches.put(queue)
                return

            queue.put_nowait(word)
            for extension in extension_list:
                if has_pattern and pattern_symbol in extension:
                    sample = extension.replace(pattern_symbol, word, 1)
                elif extension[0] == '.':
                    sample = f'{word}{extension}'
                else:
                    sample = f'{word}.{extension}'

                queue.put_nowait(sample)

            if queue.qsize() >= samples_maxsize:
                self._batches.put(queue)
                queue = Queue()

    def __len__(self):
        return self._length
