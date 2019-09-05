import argparse

from src.argument_parser.argument_manager_error import ArgumentManagerError
from src.utils.file_utils import FileUtils


class StoreWritableFilePath(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        if values is not None:
            if not FileUtils.is_writable(values):
                raise ArgumentManagerError('The file %s does not writable' % (values,))
            setattr(namespace, self.dest, values)
