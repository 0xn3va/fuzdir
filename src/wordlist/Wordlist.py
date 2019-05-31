from src.utils.FileUtils import FileUtils
from src.utils.GeneratorUtils import thread_safe_generator
from src.wordlist.Encoding import Encoding


class Wordlist:
    pattern_symbol = '%'
    _comment_symbol = b'#'

    def __init__(self, wordlist_path: str, extensions: list, extensions_file: str):
        if not FileUtils.is_readable(wordlist_path):
            raise FileExistsError('The wordlist file does not exist or access denied')
        self._wordlist_path = wordlist_path
        self._wordlist_size = sum(1 for _ in self._read_file(self._wordlist_path))
        self._extensions = []
        self._set_extensions(extensions, extensions_file)

    def _set_extensions(self, extensions: list, extensions_file: str):
        if extensions_file is not None:
            if not FileUtils.is_readable(extensions_file):
                raise FileExistsError('The extensions file does not exist or access denied')
            self._extensions.extend(self._read_file(extensions_file))

        for extension in extensions:
            extension = extension.encode()
            if extension not in self._extensions:
                self._extensions.append(extension)

    def _read_file(self, path):
        with open(path, 'rb') as file:
            for line in file:
                line = line.strip()
                # Skip comments line
                if self._is_comment(line):
                    continue
                yield Encoding.decode(line)

    def _is_comment(self, line: bytes):
        try:
            return line[0] == self._comment_symbol
        except IndexError:
            return False

    @property
    def extensions(self):
        return self._extensions

    def __len__(self):
        return self._wordlist_size * len(self._extensions) if len(self._extensions) > 0 else self._wordlist_size

    @thread_safe_generator
    def __iter__(self) -> str:
        for sample in self._read_file(self._wordlist_path):
            for ext in self._extensions:
                if self.pattern_symbol in ext:
                    yield ext.replace(self.pattern_symbol, sample, 1)
                else:
                    yield '%s.%s' % (sample, ext,)

            yield sample
