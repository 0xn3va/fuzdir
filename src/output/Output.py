import threading
from abc import ABC, abstractmethod

from colorama import init, Style, Fore, Back
from requests import Response

from src.output.MessageType import MessageType
from src.output.SplashType import SplashType
from src.utils.FileUtils import FileUtils


class Output(ABC):
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

    def __init__(self, error_log_path: str):
        init(autoreset=True)
        self._error_log_path = error_log_path
        if not FileUtils.dir_exist(self._error_log_path):
            raise FileExistsError('Logs directory is missing')
        if not FileUtils.is_writable(self._error_log_path):
            raise FileExistsError('The log directory should be writable')
        self._error_log = None
        self._cli_lock = threading.Lock()
        self._log_lock = threading.Lock()

    @abstractmethod
    def print_response(self, response: Response):
        return NotImplemented

    def print_splash(self, splash_type: SplashType, *args):
        if splash_type == SplashType.banner:
            line = self._banner_format % (args[0],)
        elif splash_type == SplashType.log_path:
            line = self._error_log_format % (self._error_log_path,)
        elif splash_type == SplashType.config:
            extensions, threads, wordlist_size = args
            line = ''
            printable_extensions = extensions[:self._config_extensions_size] if self._config_extensions_size < len(extensions) else extensions
            if len(printable_extensions) > 0:
                extensions_value = self._config_extensions_separator.join(extension for extension in printable_extensions)
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
        self.print_line(line)

    def progress_bar(self, percent: float):
        with self._cli_lock:
            self.print_line(self._progress_bar_format % (percent,), end='\r')

    def print(self, message_type: MessageType, message: str):
        if message_type == MessageType.log:
            self._print_log(message)
        elif message_type == MessageType.error:
            self._print_error(message)
        else:
            self._print_info(message)

    def _print_log(self, message: str):
        with self._log_lock:
            self.print_line(message, file=self._error_log)

    def _print_error(self, message: str):
        with self._cli_lock:
            self.print_line(self.error_message_format % (message,))

    def _print_info(self, message: str):
        with self._cli_lock:
            self.print_line(message)

    @staticmethod
    def print_line(line: str, end: str = '\n', file=None):
        print(line, flush=True, end=end, file=file)

    def __enter__(self):
        self._error_log = open(self._error_log_path, 'w')
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._error_log.close()
