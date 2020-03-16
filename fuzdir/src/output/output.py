import threading
from time import strftime

from colorama import init, Style, Fore, Back
from requests import Response
from urllib3.util import parse_url

from src.network.network_utils import NetworkUtils
from src.network.requester.utils.header_names import HeaderNames
from src.utils.singleton import Singleton


class Output(metaclass=Singleton):
    _status_code_color = {
        200: Fore.GREEN,
        301: Fore.CYAN,
        302: Fore.CYAN,
        307: Fore.CYAN,
        308: Fore.CYAN,
        401: Fore.YELLOW,
        403: Fore.BLUE
    }

    def __init__(self):
        init(autoreset=True)
        self._lock = threading.Lock()

    def banner(self, banner: str):
        self.line(f'{Style.BRIGHT}{Fore.YELLOW}{banner}{Style.RESET_ALL}')

    def summary(self, log_path: str, threads: int, method: str, dictionary_size: int, target: str):
        self.line(f'Log file: {log_path}\n')
        threads_value = f'{Fore.CYAN}{threads}{Fore.YELLOW}'
        method_value = f'{Fore.CYAN}{method.upper()}{Fore.YELLOW}'
        dictionary_value = f'{Fore.CYAN}{dictionary_size}{Fore.YELLOW}'
        self.line(f'{Style.BRIGHT}{Fore.YELLOW}Threads: {threads_value} | Method: {method_value} | Wordlist size: {dictionary_value}\n{Style.RESET_ALL}')
        target_value = f'{Fore.CYAN}{target}{Fore.YELLOW}'
        self.line(f'{Style.BRIGHT}{Fore.YELLOW}Target: {target_value}\n{Style.RESET_ALL}')

    def progress_bar(self, percent: float):
        self.line(f'{percent:.2f}%', end='\r')

    def error(self, message: str):
        self.line(f'{Style.BRIGHT}{Fore.WHITE}{Back.RED}{message}{Style.RESET_ALL}')

    def response(self, response: Response):
        status = response.status_code
        path = parse_url(response.url).path
        content_length = NetworkUtils.content_length(response)
        message = f'[{strftime("%H:%M:%S")}] {status} - {content_length:6d} - {path}'
        if response.is_redirect:
            message = f'{message}  ->  {response.headers.get(HeaderNames.location, "None")}'

        self.line(f'{self._status_code_color.get(status, "")}{message}')

    def line(self, line: str, end: str = '\n'):
        with self._lock:
            print(line, flush=True, end=end)
