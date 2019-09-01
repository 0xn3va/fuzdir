import tempfile
import unittest

from src.dictionary.extension_list import ExtensionList


class ExtensionListTest(unittest.TestCase):
    _extensions_from_args = ['txt', 'bak', 'js']
    _extensions_from_file = ['txt', 'html', 'php']

    def test_init(self):
        with tempfile.NamedTemporaryFile() as file:
            for extension in self._extensions_from_file:
                line = '%s\n' % (extension,)
                file.write(line.encode())
            file.flush()

            all_extensions = set(self._extensions_from_args)
            all_extensions.update(e for e in self._extensions_from_file)
            all_extensions = list(all_extensions)

            self.assertCountEqual(ExtensionList(self._extensions_from_args)._extensions, self._extensions_from_args,
                                  msg='Check of reading extensions from argument line failed')
            self.assertCountEqual(ExtensionList([], file.name)._extensions, self._extensions_from_file,
                                  msg='Check of reading extensions from file failed')
            self.assertCountEqual(ExtensionList(self._extensions_from_args, file.name)._extensions, all_extensions,
                                  msg='Check of merging extensions form file and argument line failed')
