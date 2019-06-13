import time

from colorama import Fore
from requests import Response
from urllib3.util import parse_url

from src.network.NetworkUtils import NetworkUtils
from src.network.request.HeaderNames import HeaderNames
from src.output.Output import Output


class CLIOutput(Output):
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

    def __init__(self, error_log_path: str):
        super(CLIOutput, self).__init__(error_log_path=error_log_path)

    def print_response(self, response: Response):
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

        with self._cli_lock:
            self.print_line(self._status_code_color.get(status, '') + message)
