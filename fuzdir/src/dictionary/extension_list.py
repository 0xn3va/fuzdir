from src.dictionary.utils.file_reader import FileReader


class ExtensionList:
    pattern_symbol = '%'

    def __init__(self, extensions: list, path: str):
        self._extensions = set(extensions)
        for extension in FileReader.read(path=path):
            if extension not in self._extensions:
                self._extensions.add(extension)

        self._extensions = list(self._extensions)
        self.has_pattern = False
        for extension in self._extensions:
            if self.pattern_symbol in extension:
                self.has_pattern = True
                break

    def __len__(self):
        return len(self._extensions)

    def __iter__(self):
        for extension in self._extensions:
            yield extension
