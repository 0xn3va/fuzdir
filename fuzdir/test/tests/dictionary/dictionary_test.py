import tempfile
import threading
import unittest
from queue import Empty

from src.dictionary.dictionary import Dictionary
from src.dictionary.extension_list import ExtensionList
from src.dictionary.word_list import WordList
from test.mocks.utils import random_string, random_int


class DictionaryTest(unittest.TestCase):
    def test_formation(self):
        extensions = ['txt', '%.bak']
        file_extensions = '.js'
        file_word = 'index'
        words = ['foo']
        formation_result = ['index', 'index.txt', 'index.bak', 'index.js', 'foo', 'foo.txt', 'foo.bak', 'foo.js']

        with tempfile.NamedTemporaryFile() as word_file, tempfile.NamedTemporaryFile() as extension_file:
            word_file.write(file_word.encode())
            word_file.flush()
            extension_file.write(file_extensions.encode())
            extension_file.flush()
            dictionary = Dictionary(word_list=WordList(words=words, path=word_file.name),
                                    extension_list=ExtensionList(extensions=extensions, path=extension_file.name))
            dictionary.samples_maxsize = 2
            samples = []
            while True:
                try:
                    samples.append(dictionary.get())
                except Empty:
                    break

        self.assertCountEqual(samples, formation_result, msg='Check of a dictionary formation failed')

    def test_massive_getting(self):
        extension_list = ExtensionList(extensions=[random_string() for _ in range(random_int(1, 3))], path=None)

        with tempfile.NamedTemporaryFile() as file:
            for _ in range(random_int(100000, 150000)):
                file.write(f'{random_string()}\n'.encode())
            file.flush()

            dictionary = Dictionary(word_list=WordList(words=[], path=file.name), extension_list=extension_list)
            count = 0
            while True:
                try:
                    _ = dictionary.get()
                    count += 1
                except Empty:
                    break

        self.assertEqual(len(dictionary), count, msg='Check of a getting samples from dictionary failed')

    def test_multi_thread_getting(self):
        extension_list = ExtensionList(extensions=[random_string() for _ in range(random_int(1, 3))], path=None)

        with tempfile.NamedTemporaryFile() as file:
            for _ in range(random_int(100000, 150000)):
                file.write(f'{random_string()}\n'.encode())
            file.flush()

            dictionary = Dictionary(word_list=WordList(words=[], path=file.name), extension_list=extension_list)
            self.count = 0
            lock = threading.Lock()

            def task():
                while True:
                    try:
                        _ = dictionary.get()
                        with lock:
                            self.count += 1
                    except Empty:
                        break

            threads = []
            for _ in range(10):
                thread = threading.Thread(target=task)
                threads.append(thread)
                thread.start()

            while any(thread.is_alive() for thread in threads):
                try:
                    for thread in threads:
                        thread.join()
                except Exception:
                    pass

        self.assertEqual(len(dictionary), self.count, msg='Check of a multi thread getting samples from dictionary failed')

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
