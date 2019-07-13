from src.wordlist.EncodingError import EncodingError


class Encoding:
    codecs = ['utf-8', 'cp1251']

    @staticmethod
    def decode(line: bytes) -> str:
        for index, encoding in enumerate(Encoding.codecs):
            try:
                return line.decode(encoding)
            except UnicodeDecodeError:
                if index == len(Encoding.codecs) - 1:
                    raise EncodingError('Unknown file encoding')


