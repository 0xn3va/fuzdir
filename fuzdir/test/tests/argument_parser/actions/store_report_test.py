import tempfile
import unittest
from pathlib import Path

from src.argument_parser.argument_manager import ArgumentManager
from src.argument_parser.argument_manager_error import ArgumentManagerError
from test.mocks.utils import random_string


class StoreReportTest(unittest.TestCase):
    def test_call(self):
        argument_manager = ArgumentManager()
        with self.assertRaises(ArgumentManagerError, msg='Check on empty path failed'):
            argument_manager.parse_args(args=['--report', 'plain'])

        with self.assertRaises(ArgumentManagerError, msg='Check on empty path failed'):
            argument_manager.parse_args(args=['--report', 'plain='])

        with self.assertRaises(ArgumentManagerError, msg='Check on writable report file failed'):
            file = tempfile.NamedTemporaryFile(mode='r')
            try:
                Path(file.name).chmod(0o555)
                argument_manager.parse_args(args=['--report', f'json={file.name}'])
            finally:
                file.close()

        with self.assertRaises(ArgumentManagerError, msg='Check on incorrect report type failed'):
            with tempfile.NamedTemporaryFile() as file:
                argument_manager.parse_args(args=['--report', f'{random_string()}={file.name}'])

        with tempfile.NamedTemporaryFile() as file:
            argument_manager.parse_args(args=['--report', f' json : body = {file.name} ', '-u http://localhost', '-w a'])
            self.assertTupleEqual(('json', file.name, ['body']), argument_manager.report_config,
                                  msg='Check on parse report config with an extra spaces failed')
