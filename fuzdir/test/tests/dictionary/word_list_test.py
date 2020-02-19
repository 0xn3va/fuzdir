import tempfile
import unittest

from src.dictionary.word_list import WordList
from test.mocks.utils import random_string, random_int


class WordListTest(unittest.TestCase):
    def test_length(self):
        words = [random_string() for _ in range(random_int())]
        file_length = random_int()
        with tempfile.NamedTemporaryFile() as file:
            for _ in range(file_length):
                line = f'{random_string()}\n'
                file.write(line.encode())
            file.flush()

            self.assertEqual(len(WordList(words=words, path=file.name)), len(words) + file_length,
                             msg='The actual wordlist length doesn\'t match with the calculated')

    def test_iter(self):
        file_words = [random_string() for _ in range(random_int())]
        words = [random_string() for _ in range(random_int())]

        with tempfile.NamedTemporaryFile() as file:
            for word in file_words:
                line = f'{word}\n'
                file.write(line.encode())
            file.flush()

            self.assertCountEqual([word for word in WordList(words=words, path=file.name)], file_words + words,
                                  msg='Check of merging words from file and argument line failed')
            self.assertCountEqual([word for word in WordList(words=words, path=None)], words,
                                  msg='Check of reading words from argument line failed')
            self.assertCountEqual([word for word in WordList(words=[], path=file.name)], file_words,
                                  msg='Check of reading words from file failed')
            self.assertFalse([word for word in WordList(words=[], path=None)],
                             msg='Checking that the wordlist is empty failed')
