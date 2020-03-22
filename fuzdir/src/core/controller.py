import logging
import time
from pathlib import Path

from src import output
from src.argument_parser.argument_manager import ArgumentManager
from src.argument_parser.argument_manager_error import ArgumentManagerError
from src.core.fuzzer import Fuzzer
from src.dictionary.extension_list import ExtensionList
from src.dictionary.word_list import WordList
from src.utils.file_utils import FileUtils
from src.dictionary.utils.encoding_error import EncodingError
from src.dictionary.dictionary import Dictionary
from src.filter.filter import Filter
from src.network.requester.requester_error import RequesterError
from src.network.requester.requester import Requester

MAJOR_VERSION = 1
MINOR_VERSION = 0
REVISION = '.3'
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
    _logs_mode = 0o755
    _logs_capacity = 32
    _log_name_prefix = 'log'

    def __init__(self, root_path: str):
        argument_manager = ArgumentManager()
        try:
            # print banner
            with open(Path(root_path).joinpath(self._banner_filename), 'r') as banner_file:
                banner = banner_file.read()
            banner = banner.format(**VERSION)
            output.banner(banner=banner)
            # parse and prepare arguments
            argument_manager.parse_args()
            # logging config
            log_path = self._logging_setup(root_path, argument_manager.verbose)
            output.setup(config=argument_manager.report_config)
            # setting main components
            dictionary = Dictionary(word_list=WordList(words=argument_manager.words, path=argument_manager.words_file),
                                    extension_list=ExtensionList(extensions=argument_manager.extensions,
                                                                 path=argument_manager.extensions_file))

            requester = Requester(url=argument_manager.url,
                                  method=argument_manager.method,
                                  user_agent=argument_manager.user_agent,
                                  cookie=argument_manager.cookie,
                                  headers=argument_manager.headers,
                                  allow_redirect=argument_manager.allow_redirect,
                                  timeout=argument_manager.timeout,
                                  retries=argument_manager.retry,
                                  status_forcelist=argument_manager.retry_status_list,
                                  raise_on_status=argument_manager.raise_on_status,
                                  throttling_period=argument_manager.throttling_period,
                                  proxy=argument_manager.proxy)

            filter = Filter(conditions=argument_manager.conditions)
            self._fuzzer = Fuzzer(dictionary=dictionary, requester=requester, filter=filter,
                                  threads=argument_manager.threads)
            # print summary
            output.summary(log_path=log_path, threads=self._fuzzer.threads, method=requester.method,
                           dictionary_size=len(dictionary), target=requester.url)
        except (IOError, PermissionError, EncodingError, ArgumentManagerError, RequesterError) as e:
            if isinstance(e, ArgumentManagerError):
                output.line(argument_manager.format_usage())
            output.error(str(e))
            exit(0)

    def _logging_setup(self, root_path: str, verbose: bool):
        # create logs folder
        path = Path(root_path).joinpath(self._logs_dirname)
        path.mkdir(mode=self._logs_mode, exist_ok=True)
        # remove old logs
        log_paths = [log_file for log_file in list(path.rglob(f'{self._log_name_prefix}*')) if log_file.is_file()]
        log_paths.sort()
        for log_path in log_paths[:max(0, len(log_paths) - self._logs_capacity)]:
            log_path.unlink()
        # log file settings
        log_path = Path(path).joinpath(f'{self._log_name_prefix}-{time.strftime("%y-%m-%d_%H-%M-%S")}.txt')
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
