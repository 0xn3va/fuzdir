import argparse

from src import output
from src.argument_parser.actions.store_readable_file_path import StoreReadableFilePath
from src.argument_parser.actions.store_writable_file_path import StoreWritableFilePath
from src.argument_parser.argument_manager_error import ArgumentManagerError
from src.argument_parser.actions.store_dict import StoreDict
from src.argument_parser.actions.store_list import StoreList
from src.core.fuzzer import Fuzzer
from src.network.requester.requester import Requester
from src.output.report.report_type import ReportType


class ArgumentManager:
    _url_help = 'target URL'
    _word_list_help = 'path to word list'
    _extensions_help = 'extension list separated by comma'
    _extensions_file_help = 'path to file with extensions'
    _threads_help_format = 'the maximum number of threads that can be used to requests, by default %d threads'
    _timeout_help_format = 'connection timeout, by default %ds.'
    _retry_help_format = 'number of attempts to connect to the server, by default %d times'
    _throttling_help = 'delay time in seconds (float) between requests sending'
    _proxy_help = 'HTTP or SOCKS5 proxy\n' \
                  + 'usage format:\n' \
                  + '   [http|socks5]://user:pass@host:port\n'
    _user_agent_help = 'custom user agent, by default setting random user agent'
    _header_help = 'pass custom header(s)'
    _allow_redirect_help = 'allow follow up to redirection'
    _logging_help = 'verbose logging'
    _plain_report_help = 'a plain text reporting about the found status code, content length and path'
    _json_report_help = 'a reporting in JSON about the found status code, content length and path'
    _conditions_help = 'conditions for responses matching\n' \
                       + 'available conditions:\n' \
                       + '  code\t\tfilter by status code\n' \
                       + '  length\tfilter by content length\n' \
                       + '  grep\t\tfilter by regex in response headers or / and body\n' \
                       + 'usage format:\n' \
                       + '  [ignore]:<condition>:[<area>]=<args>\n' \
                       + 'examples:\n' \
                       + '  code=200,500\t\tmatch responses with 200 or 500 status code\n' \
                       + '  ignore:code=404\tmatch all responses exclude with 404 status code\n' \
                       + '  length=0-1337,7331\t\tmatch all responses with content between 0 and 1337 or equals 7331\n' \
                       + '  grep=\'regex\'\t\tmatch in response headers and body\n' \
                       + '  grep:body=\'regex\'\tmatch in response body\n'
    _examples = 'examples:\n' \
                + '  fuzdir -u https://example.com -w wordlist.txt\n' \
                + '  fuzdir -u https://example.com -w wordlist.txt -e html,js,php -x code=200\n' \
                + '  fuzdir -u https://example.com -w wordlist.txt -x code=200;ignore:grep:headers=\'Auth\''

    def __init__(self):
        parser = self._create_parser()
        try:
            args = parser.parse_args()
            # necessary arguments
            self.url = args.url
            self.word_list = args.word_list
            # extensions arguments
            self.extensions = args.extensions
            self.extensions_file = args.extensions_file
            # connection arguments
            self.threads = args.threads
            self.timeout = args.timeout
            self.retry = args.retry
            self.throttling_period = args.throttling_period
            self.proxy = args.proxy
            # request arguments
            self.user_agent = args.user_agent
            self.cookie = args.cookie
            self.headers = args.headers
            self.allow_redirect = args.allow_redirect
            # logging arguments
            self.verbose = args.verbose
            # report arguments
            self.report_type = None
            self.report_path = args.plain_report or args.json_report
            if args.plain_report is not None:
                self.report_type = ReportType.plain_text
            elif args.json_report is not None:
                self.report_type = ReportType.json_report
            # filter arguments
            self.conditions = args.conditions
        except ArgumentManagerError as e:
            output.line(parser.format_usage())
            output.error(str(e))
            exit(0)

    def _create_parser(self):
        parser = argparse.ArgumentParser(prog='fuzdir', epilog=self._examples,
                                         formatter_class=argparse.RawTextHelpFormatter)
        # necessary group
        necessary_group = parser.add_argument_group('necessary parameters')
        necessary_group.add_argument('-u', '--url', dest='url', action='store', required=True, help=self._url_help)
        necessary_group.add_argument('-w', '--wordlist', dest='word_list', action=StoreReadableFilePath, required=True,
                                     metavar='PATH', help=self._word_list_help)
        # extensions group
        wordlist_group = parser.add_argument_group('extensions settings')
        wordlist_group.add_argument('-e', '--extensions', default=[], dest='extensions', action=StoreList,
                                    help=self._extensions_help)
        wordlist_group.add_argument('-E', '--extensions-file', dest='extensions_file', action=StoreReadableFilePath,
                                    metavar='PATH', help=self._extensions_file_help)
        # connection group
        connection_group = parser.add_argument_group('connection settings')
        connection_group.add_argument('-t', '--threads', type=int, default=Fuzzer.default_threads, dest='threads',
                                      action='store', help=self._threads_help_format % (Fuzzer.default_threads,))
        connection_group.add_argument('--timeout', type=int, default=Requester.default_timeout, dest='timeout',
                                      action='store', help=self._timeout_help_format % (Requester.default_timeout,))
        connection_group.add_argument('--retry', type=int, default=Requester.default_retries, dest='retry',
                                      action='store', help=self._retry_help_format % (Requester.default_retries,))
        connection_group.add_argument('--throttling', type=float, dest='throttling_period', action='store',
                                      metavar='SECONDS', help=self._throttling_help)
        connection_group.add_argument('--proxy', dest='proxy', action='store', metavar='URL', help=self._proxy_help)
        # request group
        request_group = parser.add_argument_group('request settings')
        request_group.add_argument('--user-agent', dest='user_agent', action='store', metavar='USER AGENT',
                                   help=self._user_agent_help)
        request_group.add_argument('-c', '--cookie', dest='cookie', action='store')

        request_group.add_argument('-H', '--header', default={}, dest='headers', action=StoreDict,
                                   help=self._header_help)
        request_group.add_argument('--allow-redirect', dest='allow_redirect', action='store_true',
                                   help=self._allow_redirect_help)
        # logging arguments
        logging_group = parser.add_argument_group('logging settings')
        logging_group.add_argument('-v', '--verbose', dest='verbose', action='store_true', help=self._logging_help)
        # report arguments
        report_group = parser.add_argument_group('reports settings')
        report_group = report_group.add_mutually_exclusive_group()
        report_group.add_argument('--plain-report', dest='plain_report', action=StoreWritableFilePath, metavar='PATH',
                                  help=self._plain_report_help)
        report_group.add_argument('--json-report', dest='json_report', action=StoreWritableFilePath, metavar='PATH',
                                  help=self._json_report_help)
        # filter arguments
        filter_group = parser.add_argument_group('filter')
        filter_group.add_argument('-x', default='', dest='conditions', action='store', help=self._conditions_help)

        return parser
