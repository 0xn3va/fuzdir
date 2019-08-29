from abc import ABC, abstractmethod

from requests import Response


class Report(ABC):
    def __init__(self, filename: str, mode: str = 'w', encoding: str = None):
        self._file = open(filename, mode=mode, encoding=encoding)

    def close(self):
        try:
            self._file.flush()
        except ValueError:
            # flush operation on closed file
            pass
        finally:
            self._file.close()

    def _write(self, *args):
        print(*args, flush=True, file=self._file)

    @abstractmethod
    def write(self, response: Response):
        raise NotImplementedError
