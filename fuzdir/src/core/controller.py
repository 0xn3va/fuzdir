import logging
import os
import time

from src import output
from src.argument_parser.argument_manager import ArgumentManager
from src.core.fuzzer import Fuzzer
from src.dictionary.extension_list import ExtensionList
from src.dictionary.word_list import WordList
from src.utils.file_utils import FileUtils
from src.dictionary.utils.encoding_error import EncodingError
from src.dictionary.dictionary import Dictionary
from src.filter.filter import Filter
from src.filter.filter_error import FilterError
from src.network.requester.requester_error import RequesterError
from src.network.requester.requester import Requester

MAJOR_VERSION = 0
MINOR_VERSION = 1
REVISION = '.1'
VERSION = {
    "MAJOR_VERSION": MAJOR_VERSION,
    "MINOR_VERSION": MINOR_VERSION,
    "REVISION": REVISION
}


class Controller:
    _banner_filename = 'banner.txt'
    # logging settings
    _logging_format = '%(asctime)s %(pathname)s, line:%(lineno)d - %(levelname)s - %(message)s'
    _logs_dirname = 'logs'
    _logs_capacity = 32
    _log_name_format = '%s-%s.%s'
    _log_name_prefix = 'log'
    _log_extension = 'txt'

    def __init__(self, root_path: str):
        try:
            # print banner
            with open(os.path.join(root_path, self._banner_filename), 'r') as banner_file:
                banner = banner_file.read()
            banner = banner.format(**VERSION)
            output.banner(banner=banner)
            # parse and prepare arguments
            argument_manager = ArgumentManager()
            # logging config
            log_path = self._logging_setup(root_path, argument_manager.verbose)
            output.config(report_type=argument_manager.report_type, filename=argument_manager.report_path)
            # setting main components
            dictionary = Dictionary(word_list=WordList(path=argument_manager.word_list),
                                    extension_list=ExtensionList(extensions=argument_manager.extensions,
                                                                 path=argument_manager.extensions_file))
            requester = Requester(url=argument_manager.url, user_agent=argument_manager.user_agent,
                                  cookie=argument_manager.cookie, headers=argument_manager.headers,
                                  allow_redirect=argument_manager.allow_redirect, timeout=argument_manager.timeout,
                                  retries=argument_manager.retry, throttling_period=argument_manager.throttling_period,
                                  proxy=argument_manager.proxy)
            filter = Filter(conditions=argument_manager.conditions)
            self._fuzzer = Fuzzer(dictionary=dictionary, requester=requester, filter=filter,
                                  threads=argument_manager.threads)
            # print summary
            output.summary(log_path=log_path, threads=self._fuzzer.threads, dictionary_size=len(dictionary),
                           target=requester.url)
        except (IOError, EncodingError, RequesterError, FilterError) as e:
            output.error(str(e))
            exit(0)

    def _logging_setup(self, root_path: str, verbose: bool):
        # logs folder settings
        logs_path = os.path.join(root_path, self._logs_dirname)
        if not os.path.isdir(logs_path):
            raise IOError('The logs directory is missing')
        # remove old logs
        logs = [name for name in os.listdir(logs_path)
                if name.startswith(self._log_name_prefix) and os.path.isfile(os.path.join(logs_path, name))]
        logs.sort()
        for log_name in logs[:max(0, len(logs) - self._logs_capacity)]:
            os.remove(os.path.join(logs_path, log_name))
        # log file settings
        log_path = os.path.join(logs_path, self._log_name_format %
                                (self._log_name_prefix, time.strftime('%y-%m-%d_%H-%M-%S'), self._log_extension,))
        if not FileUtils.is_writable(log_path):
            raise IOError('The log file should be writable')
        # logging settings
        # disable urllib3 logging debug level
        logging.getLogger('urllib3').setLevel(logging.WARNING)
        level = logging.DEBUG if verbose else logging.WARNING
        logging.basicConfig(level=level, filename=log_path, format=self._logging_format)

        return log_path

    def start(self):
        try:
            logging.debug('Started fuzzing')
            self._fuzzer.start()
        finally:
            logging.debug('Shutdown')
            logging.shutdown()
            output.shutdown()
