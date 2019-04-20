from os.path import isfile

from src.utils.GeneratorUtils import thread_safe_generator


class Wordlist:
    pattern_symbol = '%'

    def __init__(self, wordlist_path: str, extensions: list, extensions_file: str):
        if not isfile(wordlist_path):
            raise FileExistsError('The wordlist file does not exist')
        self._wordlist_path = wordlist_path
        self._wordlist_size = sum(1 for _ in self._read_file(self._wordlist_path))
        self._extensions = []
        self._set_extensions(extensions, extensions_file)

    def _set_extensions(self, extensions: list, extensions_file: str):
        if extensions_file is not None:
            if not isfile(extensions_file):
                raise FileExistsError('The extensions file does not exist')
            self._extensions.extend(self._read_file(extensions_file))

        for extension in extensions:
            if extension not in self._extensions:
                self._extensions.append(extension)

    def _read_file(self, path):
        with open(path, 'r') as file:
            for line in file:
                # Skip comments line
                if self._is_comment(line):
                    continue
                yield line

    def _is_comment(self, line: str):
        return line.lstrip().startswith('#')

    @property
    def extensions(self):
        return self._extensions

    @property
    def size(self):
        return self._wordlist_size * len(self._extensions) if len(self._extensions) > 0 else self._wordlist_size

    @thread_safe_generator
    def __iter__(self):
        i = 0
        for line in self._read_file(self._wordlist_path):
            sample = line.rstrip()
            i += 1
            for ext in self._extensions:
                if self.pattern_symbol in ext:
                    # If extension contains template, will replace the pattern symbol by sample
                    yield i, ext.replace(self.pattern_symbol, sample, 1)
                else:
                    # else just join sample and extension
                    yield i, '%s.%s' % (sample, ext,)

            yield i, sample
