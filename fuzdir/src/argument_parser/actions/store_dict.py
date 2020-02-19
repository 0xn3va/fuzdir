import argparse

from src.argument_parser.argument_manager_error import ArgumentManagerError


class StoreDict(argparse.Action):
    _separator = ':'

    def __call__(self, parser, namespace, values, option_string=None):
        try:
            name, value = (value.strip() for value in values.split(self._separator))
            getattr(namespace, self.dest).update({name: value})
        except ValueError:
            raise ArgumentManagerError(f'Invalid argument value: {values}')
