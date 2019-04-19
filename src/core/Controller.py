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

    def __init__(self, banner_path: str, output: CLIOutput, arg_parser: ArgumentParser):
        self._output = output
        with open(banner_path, 'r') as banner_file:
            banner = banner_file.read()
        banner = banner.format(**VERSION)

        try:
            wordlist = Wordlist(wordlist_path=arg_parser.wordlist, extensions=arg_parser.extensions, extensions_file=arg_parser.extensions_file)
            requests = Requests(url=arg_parser.url,
                                cookie=arg_parser.cookie,
                                user_agent=arg_parser.user_agent,
                                timeout=arg_parser.timeout,
                                allow_redirects=arg_parser.allow_redirect)
            filter = Filter(conditions=arg_parser.conditions, invert=arg_parser.invert)

            self._fuzzer = Fuzzer(wordlist, requests, filter, output, threads=arg_parser.threads)
            self._output.print_banner(banner)
        except (FilterError, FileExistsError, RequestError) as e:
            self._output.print_error(str(e))
            exit(0)

    def start(self):
        self._fuzzer.start()
