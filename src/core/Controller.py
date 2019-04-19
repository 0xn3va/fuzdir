from src.core.ArgumentParser import ArgumentParser
from src.core.Fuzzer import Fuzzer
from src.core.Wordlist import Wordlist
from src.filter.Filter import Filter
from src.filter.FilterException import FilterException
from src.network.RequestError import RequestError
from src.network.Requests import Requests
from src.output.CLIOutput import CLIOutput


class Controller:

    def __init__(self, output: CLIOutput, arg_parser: ArgumentParser):

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
        except (FilterException, FileExistsError, RequestError) as e:
            self._output.print_error(str(e))
            exit(0)

    def start(self):
        self._fuzzer.start()