from src.wordlist.encoding import Encoding
from src.wordlist.thread_safe_iterator import thread_safe_iterator


class Wordlist:
    _pattern_symbol = '%'
    _comment_symbol = b'#'
    _filename_format = '%s.%s'

    def __init__(self, wordlist_path: str, extensions: list, extensions_file: str = None):
        self._wordlist_path = wordlist_path
        self._wordlist_size = sum(1 for _ in self._read_file(self._wordlist_path))
        # extensions from cli and file
        self._extensions = set()
        if extensions_file is not None:
            self._extensions.extend(self._read_file(extensions_file))
        for extension in extensions:
            if extension not in self._extensions:
                self._extensions.append(extension)

    @property
    def extensions(self) -> list:
        return self._extensions

    def __len__(self):
        return self._wordlist_size + self._wordlist_size * len(self._extensions)

    @thread_safe_iterator
    def __iter__(self):
        for sample in self._read_file(self._wordlist_path):
            for extension in self._extensions:
                if self._pattern_symbol in extension:
                    yield extension.replace(self._pattern_symbol, sample, 1)
                elif extension.startswith('.'):
                    yield sample + extension
                else:
                    yield self._filename_format % (sample, extension,)
            yield sample

    def _read_file(self, path: str) -> str:
        with open(path, 'rb') as file:
            for line in file:
                line = line.strip()
                # Skip comments line
                if not line or line.startswith(self._comment_symbol):
                    continue
                yield Encoding.decode(line)
