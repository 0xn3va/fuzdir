import os
import time

from src.core.ArgumentParser import ArgumentParser
from src.core.Fuzzer import Fuzzer
from src.core.Wordlist import Wordlist
from src.filter.Filter import Filter
from src.filter.FilterError import FilterError
from src.network.RequestError import RequestError
from src.network.Requests import Requests
from src.output.CLIOutput import CLIOutput

MAJOR_VERSION = 0
MINOR_VERSION = 1
VERSION = {
    "MAJOR_VERSION": MAJOR_VERSION,
    "MINOR_VERSION": MINOR_VERSION
}


class Controller:
    _banner_file_name = 'banner.txt'
    _logs_path = 'logs'
    _error_log_path_format = 'errors-%s.txt'

    printable_extensions_size = 6

    def __init__(self, root_path: str):
        self._banner_path = os.path.join(root_path, self._banner_file_name)
        error_log_path = os.path.join(root_path,
                                      self._logs_path,
                                      self._error_log_path_format % (time.strftime('%y-%m-%d_%H-%M-%S'),))

        arg_parser = ArgumentParser()
        self._output = CLIOutput(error_log_path=error_log_path)
        try:
            wordlist = Wordlist(wordlist_path=arg_parser.wordlist,
                                extensions=arg_parser.extensions,
                                extensions_file=arg_parser.extensions_file)
            requests = Requests(url=arg_parser.url,
                                cookie=arg_parser.cookie,
                                user_agent=arg_parser.user_agent,
                                timeout=arg_parser.timeout,
                                allow_redirects=arg_parser.allow_redirect)
            filter = Filter(conditions=arg_parser.conditions, invert=arg_parser.invert)
            self._fuzzer = Fuzzer(wordlist, requests, filter, threads=arg_parser.threads)

            #
            with open(self._banner_path, 'r') as banner_file:
                banner = banner_file.read()
            banner = banner.format(**VERSION)
            self._output.print_banner(banner)
            #
            self._output.print_error_log_path()
            self._output.print_config(wordlist.extensions, self._fuzzer.threads, len(wordlist))
            self._output.print_target(requests.url)
        except (FilterError, FileExistsError, RequestError) as e:
            self._output.print_error(str(e))
            exit(0)

    def start(self):
        with self._output as output:
            self._fuzzer.start(output)
