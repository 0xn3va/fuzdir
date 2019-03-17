from src.utils.GeneratorUtils import thread_safe_generator


class Wordlist:

    pattern_symbol = '%'

    def __init__(self, wordlist_path: str, extensions):
        self._wordlist_path = wordlist_path
        self._extensions = []
        self._set_extensions(extensions)

    def _set_extensions(self, extensions):
        # append extensions from file / list from cli
        if isinstance(extensions, list):
            self._extensions.extend(extensions)
        elif isinstance(extensions, str):
            with open(extensions, 'r') as extensions_file:
                for line in extensions_file:
                    if self._is_comment(line):
                        continue
                    self._extensions.append(line)

    def _is_comment(self, line: str):
        return line.lstrip().startswith('#')

    @thread_safe_generator
    def __iter__(self):
        with open(self._wordlist_path, 'r') as wordlist_file:
            for line in wordlist_file:
                # Skip comments line
                if self._is_comment(line):
                    continue

                sample = line.rstrip()

                for ext in self._extensions:
                    if self.pattern_symbol in ext:
                        # If extension contains template, will replace the pattern symbol by sample
                        yield ext.replace(self.pattern_symbol, sample, 1)
                    else:
                        # else just join sample and extension
                        yield '%s.%s' % (sample, ext, )

                yield sample
