import tempfile
import unittest

from src.dictionary.extension_list import ExtensionList


class ExtensionListTest(unittest.TestCase):
    _extensions_from_args = ['txt', 'bak', 'js']
    _extensions_from_file = ['txt', 'html', 'php']

    def test_length(self):
        with tempfile.NamedTemporaryFile() as file:
            for extension in self._extensions_from_file:
                line = f'{extension}\n'
                file.write(line.encode())
            file.flush()

            self.assertEqual(len(ExtensionList(extensions=self._extensions_from_args, path=file.name)),
                             len(set(self._extensions_from_args + self._extensions_from_file)),
                             msg='The actual extension list length doesn\'t match with the calculated')

    def test_iter(self):
        with tempfile.NamedTemporaryFile() as file:
            for extension in self._extensions_from_file:
                line = f'{extension}\n'
                file.write(line.encode())
            file.flush()

            self.assertCountEqual([extension for extension in ExtensionList(extensions=self._extensions_from_args, path=file.name)],
                                  set(self._extensions_from_args + self._extensions_from_file),
                                  msg='Check of merging extensions from file and argument line failed')
            self.assertCountEqual([extension for extension in ExtensionList(extensions=self._extensions_from_args, path=None)],
                                  self._extensions_from_args,
                                  msg='Check of reading extensions from argument line failed')
            self.assertCountEqual([extension for extension in ExtensionList(extensions=[], path=file.name)],
                                  self._extensions_from_file,
                                  msg='Check of reading extensions from file failed')
            self.assertFalse([extension for extension in ExtensionList(extensions=[], path=None)],
                             msg='Checking that the extension list is empty failed')
