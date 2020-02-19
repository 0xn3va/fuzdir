from src.dictionary.utils.encoding import Encoding


class FileReader:
    # 35 is a code of '#' symbol
    comment_symbol = 35

    @staticmethod
    def read(path: str):
        if path is None:
            yield from ()
        else:
            comment_symbol = FileReader.comment_symbol
            decode = Encoding.decode
            with open(path, 'rb') as file:
                for line in file:
                    line = line.strip()
                    # Skip empty and commented out line
                    if not line or line[0] == comment_symbol:
                        continue
                    yield decode(line)

    @staticmethod
    def lines_count(path: str):
        return 0 if path is None else sum(1 for _ in FileReader.read(path))
