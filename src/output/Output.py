import threading
import time

from colorama import init, Style, Fore, Back
from requests import Response
from urllib3.util import parse_url

from src.network.NetworkUtils import NetworkUtils
from src.network.request.HeaderNames import HeaderNames
from src.utils.Singleton import Singleton
from src.output.SplashType import SplashType


class Output(metaclass=Singleton):
    _banner_format = Style.BRIGHT + Fore.MAGENTA + '%s' + Style.RESET_ALL
    #
    _error_log_format = 'Errors: %s\n'
    #
    _config_format = Style.BRIGHT + Fore.YELLOW + '%s' + Style.RESET_ALL
    _config_separator = Fore.MAGENTA + ' | ' + Fore.YELLOW
    _config_extensions_size = 5
    _config_extensions_separator = ', '
    _config_extensions_padding = ' ...'
    _config_extensions_format = 'Extensions: %s%s'
    _config_threads_format = 'Threads: %s%s'
    _config_wordlist_format = 'Wordlist size: %s'
    _config_values_format = Fore.CYAN + '%s' + Fore.YELLOW
    #
    _target_format = Style.BRIGHT + Fore.YELLOW + '\nTarget: %s\n' + Style.RESET_ALL
    _target_url_format = Fore.CYAN + '%s' + Fore.YELLOW
    #
    error_message_format = Style.BRIGHT + Fore.WHITE + Back.RED + '%s' + Style.RESET_ALL
    #
    _progress_bar_format = '%.2f%%'
    #
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

    def splash(self, splash_type: SplashType, *args):
        if splash_type == SplashType.banner:
            line = self._banner_format % (args[0],)
        elif splash_type == SplashType.log_path:
            line = self._error_log_format % (args[0],)
        elif splash_type == SplashType.config:
            line = ''
            extensions, threads, wordlist_size = args
            printable_extensions = extensions[:self._config_extensions_size]
            if len(printable_extensions) > 0:
                extensions_value = self._config_extensions_separator.join(ext for ext in printable_extensions)
                if len(printable_extensions) < len(extensions):
                    extensions_value += self._config_extensions_padding
                extensions_value = self._config_values_format % (extensions_value,)
                line = self._config_extensions_format % (extensions_value, self._config_separator,)
            threads_value = self._config_values_format % (str(threads),)
            wordlist_value = self._config_values_format % (str(wordlist_size),)
            line += self._config_threads_format % (threads_value, self._config_separator,)
            line += self._config_wordlist_format % (wordlist_value,)
            line = self._config_format % (line,)
        else:
            line = self._target_format % (self._target_url_format % (args[0],),)
        self.line(line)

    def progress_bar(self, percent: float):
        self.line(self._progress_bar_format % (percent,), end='\r')

    def error(self, message: str):
        self.line(self.error_message_format % (message,))

    def response(self, response: Response):
        status = response.status_code
        path = parse_url(response.url).path
        content_length = NetworkUtils.content_length(response)

        if status in (301, 302, 307) and HeaderNames.location in response.headers:
            message = self._redirect_message_format % (time.strftime('%H:%M:%S'),
                                                       status,
                                                       content_length,
                                                       path,
                                                       response.headers[HeaderNames.location],)
        else:
            message = self._message_format % (time.strftime('%H:%M:%S'),
                                              status,
                                              content_length,
                                              path,)

        self.line(self._status_code_color.get(status, '') + message)

    def line(self, line: str, end: str = '\n'):
        with self._lock:
            print(line, flush=True, end=end)
