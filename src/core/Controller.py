import logging
import os
import time

from src.core.ArgumentParser import ArgumentParser
from src.core.Fuzzer import Fuzzer
from src.output import output
from src.utils.FileUtils import FileUtils
from src.wordlist.EncodingError import EncodingError
from src.wordlist.Wordlist import Wordlist
from src.filter.Filter import Filter
from src.filter.FilterError import FilterError
from src.network.request.RequestError import RequestError
from src.network.request.Requester import Requester
from src.output.SplashType import SplashType

MAJOR_VERSION = 0
MINOR_VERSION = 1
REVISION = 'alpha1'
VERSION = {
    "MAJOR_VERSION": MAJOR_VERSION,
    "MINOR_VERSION": MINOR_VERSION,
    "REVISION": REVISION
}


class Controller:
    # logging settings
    _logging_format = '%(asctime)s %(pathname)s, line:%(lineno)d - %(levelname)s - %(message)s'
    _logs_dirname = 'logs'
    _logs_capacity = 32
    _log_name_format = '%s-%s.%s'
    _log_name_prefix = 'log'
    _log_extension = 'txt'
    #
    _banner_filename = 'banner.txt'

    def __init__(self, root_path: str):
        try:
            arg_parser = ArgumentParser()
            # logging config
            log_path = self._logging_setup(root_path, arg_parser.verbose)
            #
            wordlist = Wordlist(wordlist_path=arg_parser.wordlist,
                                extensions=arg_parser.extensions,
                                extensions_file=arg_parser.extensions_file)
            requester = Requester(url=arg_parser.url,
                                  cookie=arg_parser.cookie,
                                  user_agent=arg_parser.user_agent,
                                  timeout=arg_parser.timeout,
                                  allow_redirects=arg_parser.allow_redirect,
                                  proxy=arg_parser.proxy,
                                  throttling_period=arg_parser.throttling_period)
            filter = Filter(conditions=arg_parser.conditions)
            self._fuzzer = Fuzzer(wordlist, requester, filter, threads=arg_parser.threads)
            # format banner and print
            with open(os.path.join(root_path, self._banner_filename), 'r') as banner_file:
                banner = banner_file.read()
            banner = banner.format(**VERSION)
            output.splash(SplashType.banner, banner)
            #
            output.splash(SplashType.log_path, log_path)
            output.splash(SplashType.config, wordlist.extensions, self._fuzzer.threads, len(wordlist))
            output.splash(SplashType.target, requester.url)
        except (FilterError, NotADirectoryError, IOError, RequestError, EncodingError) as e:
            output.error(str(e))
            exit(0)

    def _logging_setup(self, root_path: str, verbose: bool):
        # logs folder settings
        logs_path = os.path.join(root_path, self._logs_dirname)
        if not os.path.isdir(logs_path):
            raise NotADirectoryError('The logs directory is missing')
        # remove old logs
        logs = [name for name in os.listdir(logs_path) if name.startswith(self._log_name_prefix) and os.path.isfile(os.path.join(logs_path, name))]
        logs.sort()
        for log_name in logs[:max(0, len(logs) - self._logs_capacity)]:
            os.remove(os.path.join(logs_path, log_name))
        # log file settings
        log_path = os.path.join(logs_path, self._log_name_format % (self._log_name_prefix, time.strftime('%y-%m-%d_%H-%M-%S'), self._log_extension,))
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
            self._fuzzer.start()
        finally:
            logging.shutdown()
