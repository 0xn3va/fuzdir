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

    printable_extensions_size = 6

    def __init__(self, banner_path: str, output: CLIOutput, arg_parser: ArgumentParser):
        self._banner_path = banner_path
        self._output = output

        try:
            wordlist = Wordlist(wordlist_path=arg_parser.wordlist, extensions=arg_parser.extensions, extensions_file=arg_parser.extensions_file)
            requests = Requests(url=arg_parser.url,
                                cookie=arg_parser.cookie,
                                user_agent=arg_parser.user_agent,
                                timeout=arg_parser.timeout,
                                allow_redirects=arg_parser.allow_redirect)
            filter = Filter(conditions=arg_parser.conditions, invert=arg_parser.invert)
            self._fuzzer = Fuzzer(wordlist, requests, filter, output, threads=arg_parser.threads)

            self._print_banner()
            self._print_config(wordlist.extensions, self._fuzzer.threads, wordlist.size)
            self._output.print_target(requests.url)
        except (FilterError, FileExistsError, RequestError) as e:
            self._output.print_error(str(e))
            exit(0)

    def _print_banner(self):
        with open(self._banner_path, 'r') as banner_file:
            banner = banner_file.read()
        banner = banner.format(**VERSION)
        self._output.print_banner(banner)

    def _print_config(self, extensions, threads, wordlist_size):
        es = len(extensions)
        pes = self.printable_extensions_size
        extensions_str = ', '.join(e for e in extensions[:pes if pes < es else es])
        if pes < es:
            extensions_str += '...'
        self._output.print_config(extensions_str, threads, wordlist_size)

    def start(self):
        self._fuzzer.start()
