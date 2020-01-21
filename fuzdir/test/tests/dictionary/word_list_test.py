import tempfile
import unittest

from src.dictionary.word_list import WordList
from test.mocks.utils import random_string, random_int


class WordListTest(unittest.TestCase):
    def test_length(self):
        length = random_int()
        with tempfile.NamedTemporaryFile() as wl_file:
            for _ in range(length):
                line = '%s\n' % (random_string(),)
                wl_file.write(line.encode())
            wl_file.flush()
            words = []
            for _ in range(length):
                words.append(random_string())

            wordlist = WordList(words=words, path=wl_file.name)
            self.assertEqual(len(wordlist), length * 2,
                             msg='The actual wordlist length doesn\'t match with the calculated')

    def test_iter(self):
        length = random_int()
        file_words = [random_string() for _ in range(length)]
        words = [random_string() for _ in range(length)]

        with tempfile.NamedTemporaryFile() as wl_file:
            for word in file_words:
                line = '%s\n' % (word,)
                wl_file.write(line.encode())
            wl_file.flush()

            wordlist = WordList(words=words, path=wl_file.name)

            self.assertCountEqual([word for word in wordlist], file_words + words,
                                  msg='The actual wordlist doesn\'t contains all expected words')

            wordlist = WordList(words=[], path=None)

            self.assertFalse([word for word in wordlist], msg='The actual wordlist should be empty')
