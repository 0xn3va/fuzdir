import random
import tempfile
import unittest

from src.dictionary.utils.file_reader import FileReader
from test.mocks.utils import random_string


class FileReaderTest(unittest.TestCase):
    def test_read(self):
        def spaces():
            return random.choice([' ', '\t']) * random.randint(0, 1)

        data = [random_string() for _ in range(10)]
        with tempfile.NamedTemporaryFile() as file:
            file.write(b'# comment line 1\n')
            file.write(b'# comment line 2\n')
            file.write(b'\n')
            for d in data:
                prefix = spaces()
                suffix = spaces()
                line = '%s%s%s\n' % (prefix, d, suffix,)
                file.write(line.encode())
            file.write(b'\n')
            file.write(b'# comment line 3\n')
            file.write(b'\n')
            file.flush()

            lines = [line for line in FileReader.read(file.name)]
            self.assertCountEqual(lines, data, msg='Check on read from file failed')

        self.assertFalse([word for word in FileReader.read(path=None)], msg='Check on read when path is None')
