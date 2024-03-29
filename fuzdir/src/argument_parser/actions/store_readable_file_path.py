import argparse

from src.argument_parser.argument_manager_error import ArgumentManagerError
from src.utils.file_utils import FileUtils


class StoreReadableFilePath(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        if values is not None:
            if not FileUtils.is_readable(values):
                raise ArgumentManagerError(f'The file {values} does not exist or access denied')
            setattr(namespace, self.dest, values)
