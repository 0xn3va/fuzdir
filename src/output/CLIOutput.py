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

    def _print_line(self, line: str):
        print(line, flush=True)
