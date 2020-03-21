import unittest

from src.argument_parser.actions.condition_parser.condition_parser_error import ConditionParserError
from src.argument_parser.actions.condition_parser.implement.grep_condition_parser import GrepConditionParser


class GrepConditionParserTest(unittest.TestCase):
    def test_parse_arguments(self):
        condition = GrepConditionParser()
        with self.assertRaises(ConditionParserError, msg='Check on invalid pattern failed'):
            condition.parse_arguments(args='[')

    def test_parse_area(self):
        condition = GrepConditionParser()
        with self.assertRaises(ConditionParserError, msg='Check on invalid grep part failed'):
            condition.parse_area(area='test')
