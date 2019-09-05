from src.dictionary.extension_list import ExtensionList
from src.dictionary.utils.thread_safe_iterator import thread_safe_iterator
from src.dictionary.word_list import WordList


class Dictionary:
    _pattern_symbol = '%'
    _filename_format = '%s.%s'

    def __init__(self, word_list: WordList, extension_list: ExtensionList,):
        self._word_list = word_list
        self._extension_list = extension_list

    def __len__(self):
        return len(self._word_list) * (len(self._extension_list) + 1)

    @thread_safe_iterator
    def __iter__(self):
        for sample in self._word_list:
            for extension in self._extension_list:
                if self._pattern_symbol in extension:
                    yield extension.replace(self._pattern_symbol, sample, 1)
                elif extension.startswith('.'):
                    yield sample + extension
                else:
                    yield self._filename_format % (sample, extension,)
            yield sample
