from src.dictionary.utils.file_reader import FileReader


class WordList:
    def __init__(self, words: list, path: str = None):
        self._words = words
        self._path = path
        self._length = len(self._words) + sum(1 for _ in FileReader.read(self._path))

    def __len__(self):
        return self._length

    def __iter__(self):
        for word in self._words:
            yield word

        yield from FileReader.read(self._path)
