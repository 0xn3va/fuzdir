from src.dictionary.utils.encoding_error import EncodingError


class Encoding:
    codecs = ('utf-8', 'cp1251')

    @staticmethod
    def decode(line: bytes) -> str:
        codecs = Encoding.codecs
        for encoding in codecs:
            try:
                return line.decode(encoding)
            except UnicodeDecodeError:
                if encoding == codecs[-1]:
                    raise EncodingError('Unknown file encoding')
