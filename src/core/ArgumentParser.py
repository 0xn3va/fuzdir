import argparse

from src.output.CLIOutput import CLIOutput


class ArgumentParser:
    _threads_default = 10
    _timeout_default = 5

    def __init__(self, output: CLIOutput):
        self._parser = argparse.ArgumentParser()
        args = self.parse_args()

        if args.url is None:
            # output.print_error('Target URL is missing, use -u <url>')
            exit(0)

        if args.wordlist is None:
            # output.print_error('Wordlist is missing, use -w <path to wordlist>')
            exit(0)

        self.url = args.url
        self.wordlist = args.wordlist
        self.threads = args.threads
        self.timeout = args.timeout
        self.extensions = args.extensions
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

        connection_group = self._parser.add_argument_group('Connection Settings')
        connection_group.add_argument('-t', '--threads', type=int, action='store', dest='threads',
                                      default=self._threads_default,
                                      help='the maximum number of threads that can be used to requests, by default %d threads' % (self._threads_default,))
        connection_group.add_argument('--timeout', type=int, action='store', dest='timeout',
                                      default=self._timeout_default,
                                      help='connection timeout, by default %ds.' % (self._timeout_default,))

        wordlist_group = self._parser.add_argument_group('Wordlist Settings')
        wordlist_group.add_argument('-e', '--extensions', action='store', dest='extensions',
                                    help='extension list separated by comma or path to file with extensions')

        request_group = self._parser.add_argument_group('Request Settings')
        request_group.add_argument('--user-agent', type=str, action='store', dest='user_agent',
                                   help='custom user agent, by default setting random user agent')
        request_group.add_argument('-c', '--cookie', type=str, action='store', dest='cookie')
        request_group.add_argument('--allow-redirect', action='store_true', dest='allow_redirect')

        filter_group = self._parser.add_argument_group('Filter')
        filter_group.add_argument('-x', type=str, action='store', dest='conditions',
                                  metavar='condition1=args1;condition2=args2;',
                                  help='conditions for responses matching')
        filter_group.add_argument('-v', action='store_true', dest='invert', help='select non-matching responses')

        return self._parser.parse_args()
