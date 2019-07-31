import os
import random
import string
import unittest
import tempfile

from src.utils.file_utils import FileUtils


class FileUtilsTest(unittest.TestCase):
    _symbols = string.ascii_letters + string.digits
    _name_length = 10

    def test_is_writable(self):
        def dir_writable():
            with tempfile.TemporaryDirectory() as temp_dirname:
                temp_file = tempfile.NamedTemporaryFile(prefix=os.path.join(temp_dirname, ''))
                try:
                    os.chmod(temp_dirname, mode=0o555)
                    is_writable = FileUtils.is_writable(temp_file.name)
                    os.chmod(temp_dirname, mode=0o777)
                    os.chmod(temp_file.name, mode=0o777)
                finally:
                    temp_file.close()
            return is_writable

        def is_file():
            with tempfile.TemporaryDirectory() as temp_dirname:
                return FileUtils.is_writable(temp_dirname)

        def file_writable():
            temp_file = tempfile.NamedTemporaryFile()
            try:
                os.chmod(temp_file.name, mode=0o555)
                is_writable = FileUtils.is_writable(temp_file.name)
                os.chmod(temp_file.name, mode=0o777)
            finally:
                temp_file.close()
            return is_writable

        self.assertFalse(dir_writable(), msg='Check on write permissions to parent directory failed')
        self.assertTrue(FileUtils.is_writable(self._get_fake_filename()), msg='Check on file missing failed')
        self.assertFalse(is_file(), msg='Check on that this is indeed a file failed')
        self.assertFalse(file_writable(), msg='Check on write permissions to file failed')

    def test_is_readable(self):
        def file_readable():
            temp_file = tempfile.NamedTemporaryFile()
            try:
                os.chmod(temp_file.name, mode=0o333)
                is_readable = FileUtils.is_readable(temp_file.name)
                os.chmod(temp_file.name, mode=0o777)
            finally:
                temp_file.close()
            return is_readable

        def is_file():
            with tempfile.TemporaryDirectory() as temp_dirname:
                return FileUtils.is_readable(temp_dirname)

        self.assertFalse(file_readable(), msg='Check on read permissions to file failed')
        self.assertTrue(FileUtils.is_readable(self._get_fake_filename()), msg='Check on file missing failed')
        self.assertFalse(is_file(), msg='Check on that this is indeed a file failed')

    def _get_fake_filename(self):
        while True:
            filename = os.path.join(tempfile.gettempdir(),
                                    ''.join(random.choice(self._symbols) for _ in range(self._name_length)))
            if os.path.exists(filename):
                continue
            return filename
