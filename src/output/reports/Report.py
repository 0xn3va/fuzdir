from abc import ABC, abstractmethod

from requests import Response

from src.utils.FileUtils import FileUtils


class Report(ABC):
    def __init__(self, filename: str, mode: str = 'w', encoding: str = None):
        if not FileUtils.is_writable(filename):
            raise IOError('The report file should be writable')
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
