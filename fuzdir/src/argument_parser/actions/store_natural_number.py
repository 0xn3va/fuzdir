import argparse

from src.argument_parser.argument_manager_error import ArgumentManagerError


class StoreNaturalNumber(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        try:
            value = int(values)
            if value <= 0:
                raise ValueError
            setattr(namespace, self.dest, value)
        except ValueError:
            raise ArgumentManagerError(f'Argument with value: {values} must be an integer and above zero')
