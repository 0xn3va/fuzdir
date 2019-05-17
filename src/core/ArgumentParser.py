import argparse

from src.output.Output import Output


class ArgumentParser:
    _threads_default = 10
    _timeout_default = 5

    def __init__(self):
        self._parser = argparse.ArgumentParser()
        args = self.parse_args()

        if args.url is None:
            Output.print_line(Output.error_message_format % ('Target URL is missing, use -u <url>',))
            exit(0)

        if args.wordlist is None:
            Output.print_line(Output.error_message_format % ('Wordlist is missing, use -w <path to wordlist>',))
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
        self.conditions = args.conditions
        self.invert = args.invert

    def parse_args(self):
        necessary_group = self._parser.add_argument_group('Necessary Parameters')
        necessary_group.add_argument('-u', '--url', type=str, action='store', dest='url', help='target URL')
        necessary_group.add_argument('-w', '--wordlist', type=str, action='store', dest='wordlist',
                                     help='path to wordlist')

        wordlist_group = self._parser.add_argument_group('Wordlist Settings')
        wordlist_group.add_argument('-e', '--extensions', type=str, action='store', dest='extensions',
                                    help='extension list separated by comma')
        wordlist_group.add_argument('--ef', '--extensions-file', type=str, action='store', dest='extensions_file',
                                    help='path to file with extensions')

        connection_group = self._parser.add_argument_group('Connection Settings')
        connection_group.add_argument('-t', '--threads', type=int, action='store', dest='threads',
                                      default=self._threads_default,
                                      help='the maximum number of threads that can be used to requests, by default %d threads' % (self._threads_default,))
        connection_group.add_argument('--timeout', type=int, action='store', dest='timeout',
                                      default=self._timeout_default,
                                      help='connection timeout, by default %ds.' % (self._timeout_default,))

        request_group = self._parser.add_argument_group('Request Settings')
        request_group.add_argument('--user-agent', type=str, action='store', dest='user_agent',
                                   help='custom user agent, by default setting random user agent')
        request_group.add_argument('-c', '--cookie', type=str, action='store', dest='cookie')
        request_group.add_argument('--allow-redirect', action='store_true', dest='allow_redirect',
                                   help='allow follow up to redirection')

        filter_group = self._parser.add_argument_group('Filter')
        filter_group.add_argument('-x', type=str, action='store', dest='conditions',
                                  metavar='condition1=args1;invert:condition2=args2;condition3:cond_args3=args3;',
                                  default='', help='conditions for responses matching')

        return self._parser.parse_args()
