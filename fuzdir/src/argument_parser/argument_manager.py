import argparse

from src.argument_parser.actions.store_conditions import StoreConditions
from src.argument_parser.actions.store_natural_number import StoreNaturalNumber
from src.argument_parser.actions.store_readable_file_path import StoreReadableFilePath
from src.argument_parser.actions.store_dict import StoreDict
from src.argument_parser.actions.store_list import StoreList
from src.argument_parser.actions.store_report import StoreReport
from src.core.fuzzer import Fuzzer
from src.network.requester.requester import Requester


class ArgumentManager:
    _url_help = 'target URL'
    _words_help = 'a comma-separated list of words'
    _words_file_help = 'path to word list'
    _extensions_help = 'extension list separated by comma'
    _extensions_file_help = 'path to file with extensions'
    _method_help = f'HTTP method to use^ by default is {Requester.default_http_method}'
    _threads_help = f'the maximum number of threads that can be used to requests, ' \
                    f'by default {Fuzzer.default_threads} threads'
    _timeout_help = f'connection timeout, by default {Requester.default_timeout}s.'
    _retry_help = f'number of attempts to connect to the server, by default {Requester.default_retries} times'
    _retry_status_list_help = f'a comma-separated list of HTTP status codes for which should be retry on, ' \
                              f'by default {", ".join([str(s) for s in Requester.default_status_list])}'
    _ignore_retry_fail_help = 'ignore failed attempts to connect to server and continue fuzzing'
    _throttling_help = 'delay time in seconds (float) between requests sending, ' \
                       'if the throttling value is not specified, it will automatically adjust during fuzzing'
    _proxy_help = 'HTTP or SOCKS5 proxy\n' \
                  'usage format:\n' \
                  '  [http|socks5]://user:pass@host:port\n'
    _user_agent_help = 'custom user agent, by default setting random user agent'
    _header_help = 'pass custom header(s)'
    _allow_redirect_help = 'allow follow up to redirection'
    _logging_help = 'verbose logging'
    _report_help = 'reports on responses\n' \
                   'available types:\n' \
                   '  plain\t\ta plain text reporting\n' \
                   '  json\t\ta reporting in JSON\n' \
                   'usage format:\n' \
                   '  <type>[:components]=<path>\n' \
                   'available components:\n' \
                   '  json:\n' \
                   '    body\ta response body\n' \
                   '    length\ta response content length\n' \
                   '    headers\ta response headers\n' \
                   '    code\ta response status code\n' \
                   'examples:\n' \
                   '  plain=/tmp/report.txt\t\t\ta plain text reporting about the found status code, content length and path\n' \
                   '  json=/tmp/report.json\t\t\ta reporting in JSON about the found status code, content length and path\n' \
                   '  json:code,body=/tmp/report.json\ta reporting in JSON about the found status code, body and path\n'
    _conditions_help = 'conditions for responses matching\n' \
                       'available conditions:\n' \
                       '  code\t\tfilter by status code\n' \
                       '  length\tfilter by content length\n' \
                       '  grep\t\tfilter by regex in response headers or / and body\n' \
                       'usage format:\n' \
                       '  [ignore:]<condition>[:<area>]=<args>[;]\n' \
                       'examples:\n' \
                       '  code=200,500\t\t\tmatch responses with 200 or 500 status code\n' \
                       '  ignore:code=404\t\tmatch responses exclude with 404 status code\n' \
                       '  length=0-1337,7331\t\tmatch responses with content length between 0 and 1337 or equals 7331\n' \
                       '  grep=\'regex\'\t\t\tmatch responses with \'regex\' in headers or body\n' \
                       '  grep:body=\'regex\'\t\tmatch responses with \'regex\' in body\n' \
                       '  code=200;length=0-1337\tmatch responses with 200 status code and content length between 0 and 1337\n'
    _examples = 'examples:\n' \
                + '  fuzdir -u https://example.com -W wordlist.txt\n' \
                + '  fuzdir -u https://example.com -w index,robots -e html,txt\n' \
                + '  fuzdir -u https://example.com -W wordlist.txt -e html,js,php -x code=200\n' \
                + '  fuzdir -u https://example.com -W wordlist.txt -x code=200;ignore:grep:headers=\'Auth\''

    def __init__(self):
        self._parser = self._create_parser()
        self._args = None

    def _create_parser(self):
        parser = argparse.ArgumentParser(prog='fuzdir', epilog=self._examples,
                                         formatter_class=argparse.RawTextHelpFormatter)
        # necessary group
        necessary_group = parser.add_argument_group('necessary arguments')
        necessary_group.add_argument('-u', '--url', dest='url', action='store', required=True, help=self._url_help)
        necessary_group = necessary_group.add_mutually_exclusive_group(required=True)
        necessary_group.add_argument('-w', '--wordlist', default=[], dest='words', action=StoreList, metavar='WORDS',
                                     help=self._words_help)
        necessary_group.add_argument('-W', '--wordlist-path', dest='words_file', action=StoreReadableFilePath,
                                     metavar='PATH', help=self._words_file_help)
        # extensions group
        extension_group = parser.add_argument_group('extensions settings')
        extension_group.add_argument('-e', '--extensions', default=[], dest='extensions', action=StoreList,
                                     help=self._extensions_help)
        extension_group.add_argument('-E', '--extensions-file', dest='extensions_file', action=StoreReadableFilePath,
                                     metavar='PATH', help=self._extensions_file_help)
        # connection group
        connection_group = parser.add_argument_group('connection settings')
        connection_group.add_argument('-m', '--method', default=Requester.default_http_method, dest='method',
                                      action='store', help=self._method_help)
        connection_group.add_argument('-t', '--threads', default=Fuzzer.default_threads, dest='threads',
                                      action=StoreNaturalNumber, help=self._threads_help)
        connection_group.add_argument('--timeout', type=int, default=Requester.default_timeout, dest='timeout',
                                      action='store', help=self._timeout_help)
        connection_group.add_argument('--retry', type=int, default=Requester.default_retries, dest='retry',
                                      action='store', help=self._retry_help)
        connection_group.add_argument('--retry-status-list', default=Requester.default_status_list,
                                      dest='retry_status_list', action=StoreList, metavar='STATUS_LIST',
                                      help=self._retry_status_list_help)
        connection_group.add_argument('--ignore-retry-fail', dest='raise_on_status', action='store_false',
                                      help=self._ignore_retry_fail_help)
        connection_group.add_argument('--throttling', default=0, type=float, dest='throttling_period', action='store',
                                      metavar='SECONDS', nargs='?', const=None, help=self._throttling_help)
        connection_group.add_argument('--proxy', dest='proxy', action='store', metavar='URL', help=self._proxy_help)
        # request group
        request_group = parser.add_argument_group('request settings')
        request_group.add_argument('--user-agent', dest='user_agent', action='store', metavar='USER AGENT',
                                   help=self._user_agent_help)
        request_group.add_argument('-c', '--cookie', dest='cookie', action='store')
        request_group.add_argument('-H', '--header', default={}, dest='headers', action=StoreDict, metavar='HEADER',
                                   help=self._header_help)
        request_group.add_argument('--allow-redirect', dest='allow_redirect', action='store_true',
                                   help=self._allow_redirect_help)
        # logging arguments
        logging_group = parser.add_argument_group('logging settings')
        logging_group.add_argument('-v', '--verbose', dest='verbose', action='store_true', help=self._logging_help)
        # report arguments
        report_group = parser.add_argument_group('reports settings')
        report_group.add_argument('--report', dest='report_config', action=StoreReport, metavar='CONFIG',
                                  help=self._report_help)
        # filter arguments
        filter_group = parser.add_argument_group('filter')
        filter_group.add_argument('-x', default='', dest='conditions', action=StoreConditions,
                                  help=self._conditions_help)

        return parser

    def parse_args(self, args=None, namespace=None):
        self._args = self._parser.parse_args(args, namespace)
        self._args.retry_status_list = set(self._args.retry_status_list)

    def format_usage(self):
        return self._parser.format_usage()

    def __getattr__(self, item):
        try:
            return getattr(self._args, item)
        except AttributeError:
            raise AttributeError(f'\'ArgumentManager\' object has no attribute \'{item}\'')
