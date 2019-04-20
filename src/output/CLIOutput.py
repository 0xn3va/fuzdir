import threading
import time

from colorama import Fore, init, Style, Back
from requests import Response
from urllib3.util import parse_url

from src.network.utils import Headers


class CLIOutput:
    _message_format = '[%s] %d - %6d - %s'
    _redirect_message_format = '[%s] %d - %6d - %s  ->  %s'
    _status_code_color = {
        200: Fore.GREEN,
        301: Fore.CYAN,
        302: Fore.CYAN,
        307: Fore.CYAN,
        401: Fore.YELLOW,
        403: Fore.BLUE
    }

    def __init__(self):
        init(autoreset=True)
        self._lock = threading.Lock()

    def print_response(self, response: Response):
        with self._lock:
            status = response.status_code
            path = parse_url(response.url).path

            try:
                content_length = int(response.headers[Headers.content_length])
            except (KeyError, ValueError):
                # length of responses body
                content_length = len(response.content)

            if status in (301, 302, 307) and Headers.location in response.headers:
                message = self._redirect_message_format % (
                    time.strftime('%H:%M:%S'), status, content_length, path, response.headers[Headers.location])
            else:
                message = self._message_format % (time.strftime('%H:%M:%S'), status, content_length, path,)

            color = self._status_code_color.get(status, '')

            self._print_line(color + message)

    def print_error(self, message):
        with self._lock:
            self._print_line(Style.BRIGHT + Fore.WHITE + Back.RED + message)

    def print_banner(self, message):
        self._print_line(Style.BRIGHT + Fore.MAGENTA + message + Style.RESET_ALL)

    def print_config(self, extensions: str, threads: int, wordlist_size: int):
        separator = Fore.MAGENTA + ' | ' + Fore.YELLOW
        config = Style.BRIGHT + Fore.YELLOW
        if len(extensions) > 0:
            config += 'Extensions: %s%s' % (Fore.CYAN + extensions + Fore.YELLOW, separator,)
        config += 'Threads: %s%s' % (Fore.CYAN + str(threads) + Fore.YELLOW, separator,)
        config += 'Wordlist size: %s' % (Fore.CYAN + str(wordlist_size) + Fore.YELLOW,)
        config += Style.RESET_ALL
        self._print_line(config)

    def print_target(self, url):
        target = Style.BRIGHT + Fore.YELLOW
        target += '\nTarget: {0}\n'.format(Fore.CYAN + url + Fore.YELLOW)
        target += Style.RESET_ALL
        self._print_line(target)

    def progress_bar(self, percent):
        with self._lock:
            self._print_line('%.2f%s' % (percent, '%', ), end='\r')

    def _print_line(self, line: str, end: str = '\n'):
        print(line, flush=True, end=end)
