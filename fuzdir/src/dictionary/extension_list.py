from src.dictionary.utils.file_reader import FileReader


class ExtensionList:
    def __init__(self, extensions: list, path: str = None):
        self._extensions = set()
        if path is not None:
            self._extensions.update(e for e in FileReader.read(path))
        self._extensions.update(e for e in extensions if e and e not in self._extensions)
        self._extensions = list(self._extensions)

    def __len__(self):
        return len(self._extensions)

    def __iter__(self):
        for extension in self._extensions:
            yield extension
