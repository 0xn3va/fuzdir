import argparse

from src.argument_parser.argument_parser_error import ArgumentParserError


class StoreDict(argparse.Action):
    _separator = ':'
    _message_format = 'Invalid argument: %s'

    def __call__(self, parser, namespace, values, option_string=None):
        try:
            name, value = values.split(self._separator)
            getattr(namespace, self.dest).update({name: value})
        except ValueError:
            raise ArgumentParserError(self._message_format % (values,))
