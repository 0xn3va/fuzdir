from src.dictionary.utils.file_reader import FileReader


class WordList:
    def __init__(self, words: list, path: str):
        self._words = words
        self._path = path
        self._length = len(words) + FileReader.lines_count(path=path)

    def __len__(self):
        return self._length

    def __iter__(self):
        for word in self._words:
            yield word

        yield from FileReader.read(path=self._path)
