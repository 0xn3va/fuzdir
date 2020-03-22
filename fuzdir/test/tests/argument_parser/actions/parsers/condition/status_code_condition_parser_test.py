import unittest

from src.argument_parser.actions.parsers.condition.condition_parser_error import ConditionParserError
from src.argument_parser.actions.parsers.condition.implement.status_code_condition_parser import \
    StatusCodeConditionParser


class StatusCodeConditionParserTest(unittest.TestCase):
    def test_parse_arguments(self):
        condition = StatusCodeConditionParser()
        with self.assertRaises(ConditionParserError, msg='Check on parse arguments with non number failed'):
            condition.parse_arguments(args='a,a')

        with self.assertRaises(ConditionParserError, msg='Check on parse arguments with incorrect status code failed'):
            condition.parse_arguments(args='0')

        arguments = condition.parse_arguments(args='200,404,')
        self.assertListEqual(arguments, [(200, 200), (404, 404)],
                             msg='Check on parse arguments with separator in the end line failed')

    def test_parse_area(self):
        condition = StatusCodeConditionParser()
        with self.assertRaises(ConditionParserError, msg='Check on parse arguments area with non empty value failed'):
            condition.parse_area(area='body')
