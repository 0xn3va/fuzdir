from src.dictionary.utils.encoding import Encoding


class FileReader:
    comment_symbol = b'#'

    @staticmethod
    def read(path: str = None):
        if path is None:
            yield from ()
            return

        with open(path, 'rb') as file:
            for line in file:
                line = line.strip()
                # Skip empty and commented out line
                if not line or line.startswith(FileReader.comment_symbol):
                    continue
                yield Encoding.decode(line)
