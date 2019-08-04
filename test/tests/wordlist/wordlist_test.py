import random
import tempfile
import unittest

from src.wordlist.wordlist import Wordlist


class WordlistTest(unittest.TestCase):

    _arg_ext = ['txt', '%.bak', '.js']
    _file_ext = ['txt', 'html', 'php']
    _file_wl = ['index', 'login', 'config']
    _file_formation_result = ['index', 'index.txt', 'index.bak', 'index.js']

    def test_extensions(self):
        def spaces():
            return random.choice([' ', '\t']) * random.randint(0, 1)

        with tempfile.NamedTemporaryFile() as wl_file, tempfile.NamedTemporaryFile() as ext_file:
            ext_file.write(b'# comment line 1\n')
            ext_file.write(b'# comment line 2\n')
            for extension in self._file_ext:
                prefix = spaces()
                suffix = spaces()
                line = '%s%s%s\n' % (prefix, extension, suffix,)
                ext_file.write(line.encode())
            ext_file.write(b'# comment line 3\n')
            ext_file.flush()

            all_ext = list(self._arg_ext)
            all_ext.extend(e for e in self._file_ext if e not in self._arg_ext)

            self.assertCountEqual(Wordlist(wl_file.name, self._arg_ext).extensions, self._arg_ext,
                                  msg='Check of reading extensions from argument line failed')
            self.assertCountEqual(Wordlist(wl_file.name, [], ext_file.name).extensions, self._file_ext,
                                  msg='Check of reading extensions from file failed')
            self.assertCountEqual(Wordlist(wl_file.name, self._arg_ext, ext_file.name).extensions, all_ext,
                                  msg='Check of merging extensions form file and argument line failed')

    def test_formation(self):
        with tempfile.NamedTemporaryFile() as wl_file:
            wl_file.write(self._file_wl[0].encode())
            wl_file.flush()
            wl = Wordlist(wl_file.name, self._arg_ext)
            for sample in wl:
                self.assertIn(sample, self._file_formation_result, msg='Check of a wordlist formation failed')

    def test_length(self):
        with tempfile.NamedTemporaryFile() as wl_file, tempfile.NamedTemporaryFile() as ext_file:
            for word in self._file_wl:
                wl_file.write(word.encode())
            wl_file.flush()
            for extension in self._file_ext:
                ext_file.write(extension.encode())
            ext_file.flush()
            wl = Wordlist(wl_file.name, self._arg_ext, ext_file.name)
            self.assertEqual(sum(1 for _ in wl), len(wl),
                             msg='The actual wordlist length doesn\'t match with the calculated')
