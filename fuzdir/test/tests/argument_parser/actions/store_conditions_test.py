import unittest

from src.argument_parser.argument_manager import ArgumentManager
from src.argument_parser.argument_manager_error import ArgumentManagerError


class StoreConditionsTest(unittest.TestCase):
    def test_call(self):
        argument_manager = ArgumentManager()
        with self.assertRaises(ArgumentManagerError, msg='Check on empty args failed'):
            argument_manager.parse_args(args=['-x condition='])

        with self.assertRaises(ArgumentManagerError, msg='Check on prefix for ignoring failed'):
            argument_manager.parse_args(args=['-x not_ignore:condition=args'])

        with self.assertRaises(ArgumentManagerError, msg='Check on incorrect condition name failed'):
            argument_manager.parse_args(args=['-x condition=args'])

        with self.assertRaises(ArgumentManagerError, msg='Check on incorrect arguments for condition setup failed'):
            argument_manager.parse_args(args=['-x code=0'])

        with self.assertRaises(ArgumentManagerError, msg='Check on incorrect area for condition setup failed'):
            argument_manager.parse_args(args=['-x grep:area=args'])
