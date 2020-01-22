import tempfile
import unittest

from src.dictionary.dictionary import Dictionary
from src.dictionary.extension_list import ExtensionList
from src.dictionary.word_list import WordList
from test.mocks.utils import random_string, random_int


class DictionaryTest(unittest.TestCase):
    def test_formation(self):
        extensions = ['txt', '%.bak', '.js']
        file_word = 'index'
        words = ['foo']
        formation_result = ['index', 'index.txt', 'index.bak', 'index.js', 'foo', 'foo.txt', 'foo.bak', 'foo.js']

        with tempfile.NamedTemporaryFile() as file:
            file.write(file_word.encode())
            file.flush()
            dictionary = Dictionary(WordList(words=words, path=file.name), ExtensionList(extensions=extensions))
            samples = [sample for sample in dictionary]

        self.assertCountEqual(samples, formation_result, msg='Check of a dictionary formation failed')

    def test_length(self):
        length = random_int()
        words = [random_string() for _ in range(length)]
        extensions = [random_string(k=3) for _ in range(length)]
        with tempfile.NamedTemporaryFile() as wl_file, tempfile.NamedTemporaryFile() as ext_file:
            for _ in range(length):
                line = '%s\n' % (random_string(),)
                wl_file.write(line.encode())
            wl_file.flush()

            for _ in range(length):
                line = '%s\n' % (random_string(k=3),)
                ext_file.write(line.encode())
            ext_file.flush()

            dictionary = Dictionary(word_list=WordList(words=words, path=wl_file.name),
                                    extension_list=ExtensionList(extensions=extensions, path=ext_file.name))

            self.assertEqual(len(dictionary), (length * 2) * (length * 2 + 1),
                             msg='The actual dictionary length doesn\'t match with the calculated')
