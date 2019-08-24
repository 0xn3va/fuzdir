import argparse

from src.argument_parser.argument_parser_error import ArgumentParserError
from src.utils.file_utils import FileUtils


class StoreReadableFilePath(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        if values is not None:
            if not FileUtils.is_readable(values):
                raise ArgumentParserError('The file %s does not exist or access denied' % (values,))
            setattr(namespace, self.dest, values)
