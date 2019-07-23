import argparse

from src import output


class ArgumentParser:
    _threads_default = 10
    _timeout_default = 5
    _examples = 'examples:\n' \
                + '  dirb -u https://example.com -w wordlist.txt\n' \
                + '  dirb -u https://example.com -w wordlist.txt -e html,js,php -x code=200\n' \
                + '  dirb -u https://example.com -w wordlist.txt -x code=200;ignore:grep:headers=\'Auth\''

    def __init__(self):
        self._parser = argparse.ArgumentParser(prog='dirb',
                                               epilog=self._examples,
                                               formatter_class=argparse.RawTextHelpFormatter)
        args = self.parse_args()

        if args.url is None:
            output.error('Target URL is missing, use -u <url>')
            exit(0)

        if args.wordlist is None:
            output.error('Wordlist is missing, use -w <path to wordlist>')
            exit(0)

        self.url = args.url
        self.wordlist = args.wordlist
        self.threads = args.threads
        self.timeout = args.timeout
        self.extensions = [] if args.extensions is None else args.extensions.split(',')
        self.extensions_file = args.extensions_file
        self.user_agent = args.user_agent
        self.cookie = args.cookie
        self.allow_redirect = args.allow_redirect
        self.throttling_period = args.throttling_period
        self.proxy = args.proxy
        self.conditions = args.conditions
        self.verbose = args.verbose

    def parse_args(self):
        necessary_group = self._parser.add_argument_group('necessary parameters')
        necessary_group.add_argument('-u', '--url', type=str, action='store', dest='url', help='target URL')
        necessary_group.add_argument('-w', '--wordlist', type=str, action='store', dest='wordlist',
                                     help='path to wordlist')

        wordlist_group = self._parser.add_argument_group('wordlist settings')
        wordlist_group.add_argument('-e', '--extensions', type=str, action='store', dest='extensions',
                                    help='extension list separated by comma')
        wordlist_group.add_argument('--ef', '--extensions-file', type=str, action='store', dest='extensions_file',
                                    help='path to file with extensions')

        connection_group = self._parser.add_argument_group('connection settings')
        connection_group.add_argument('-t', '--threads', type=int, action='store', dest='threads',
                                      default=self._threads_default,
                                      help='the maximum number of threads that can be used to requests, by default %d threads' % (
                                          self._threads_default,))
        connection_group.add_argument('--timeout', type=int, action='store', dest='timeout',
                                      default=self._timeout_default,
                                      help='connection timeout, by default %ds.' % (self._timeout_default,))
        connection_group.add_argument('--throttling', type=float, action='store', dest='throttling_period',
                                      default=None, help='delay time in seconds (float) between requests sending')
        connection_group.add_argument('--proxy', type=str, action='store', dest='proxy', default=None,
                                      help='HTTP or SOCKS5 proxy\n'
                                      + 'usage format:\n'
                                      + '   [http|socks5]://user:pass@host:port\n')

        request_group = self._parser.add_argument_group('request settings')
        request_group.add_argument('--user-agent', type=str, action='store', dest='user_agent',
                                   help='custom user agent, by default setting random user agent')
        request_group.add_argument('-c', '--cookie', type=str, action='store', dest='cookie')
        request_group.add_argument('--allow-redirect', action='store_true', dest='allow_redirect',
                                   help='allow follow up to redirection')

        logging_group = self._parser.add_argument_group('logging settings')
        logging_group.add_argument('-v', '--verbose', action='store_true', dest='verbose',
                                   help='verbose logging')

        filter_group = self._parser.add_argument_group('filter')
        filter_group.add_argument('-x', type=str, action='store', dest='conditions', default='',
                                  help='conditions for responses matching\n'
                                       + 'available conditions:\n'
                                       + '  code\t\tfilter by status code\n'
                                       + '  length\tfilter by content length\n'
                                       + '  grep\t\tfilter by regex in response headers or / and body\n'
                                       + 'usage format:\n'
                                       + '  [ignore]:<condition>:[<mode>]=<args>\n'
                                       + 'examples:\n'
                                       + '  code=200,500\t\tmatch responses with 200 or 500 status code\n'
                                       + '  ignore:code=404\tmatch all responses exclude with 404 status code\n'
                                       + '  length=1337\t\tmatch all responses with content length equals 1337\n'
                                       + '  length=0-1337\t\tmatch all responses with content length between 0 and 1337\n'
                                       + '  grep=\'regex\'\t\tmatch in response headers and body\n'
                                       + '  grep:body=\'regex\'\tmatch in response body\n')

        return self._parser.parse_args()
