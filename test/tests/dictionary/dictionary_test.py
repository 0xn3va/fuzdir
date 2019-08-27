import tempfile
import unittest

from src.dictionary.dictionary import Dictionary
from src.dictionary.extension_list import ExtensionList
from src.dictionary.word_list import WordList
from test.mocks.utils import random_string


class DictionaryTest(unittest.TestCase):
    def test_formation(self):
        extensions = ['txt', '%.bak', '.js']
        word = 'index'
        formation_result = ['index', 'index.txt', 'index.bak', 'index.js']

        with tempfile.NamedTemporaryFile() as file:
            file.write(word.encode())
            file.flush()
            dictionary = Dictionary(WordList(path=file.name), ExtensionList(extensions=extensions))
            samples = [sample for sample in dictionary]
            self.assertCountEqual(samples, formation_result, msg='Check of a dictionary formation failed')

    def test_length(self):
        extensions = [random_string(k=3) for _ in range(5)]
        with tempfile.NamedTemporaryFile() as wl_file, tempfile.NamedTemporaryFile() as ext_file:
            for _ in range(10):
                wl_file.write(random_string().encode())
            wl_file.flush()
            for _ in range(10):
                ext_file.write(random_string(k=3).encode())
            ext_file.flush()
            dictionary = Dictionary(word_list=WordList(path=wl_file.name),
                                    extension_list=ExtensionList(extensions=extensions, path=ext_file.name))
            self.assertEqual(sum(1 for _ in dictionary), len(dictionary),
                             msg='The actual dictionary length doesn\'t match with the calculated')
