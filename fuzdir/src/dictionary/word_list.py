from src.dictionary.utils.file_reader import FileReader


class WordList:
    def __init__(self, path: str):
        self._path = path
        self._length = sum(1 for _ in FileReader.read(self._path))

    def __len__(self):
        return self._length

    def __iter__(self):
        return FileReader.read(self._path)
