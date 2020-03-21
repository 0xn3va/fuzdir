import unittest

from src.argument_parser.actions.condition_parser.condition_parser_error import ConditionParserError
from src.argument_parser.actions.condition_parser.implement.content_length_condition_parser import \
    ContentLengthConditionParser


class ContentLengthConditionParserTest(unittest.TestCase):
    def test_parse_arguments(self):
        condition = ContentLengthConditionParser()
        with self.assertRaises(ConditionParserError, msg='Check on setup with empty line failed'):
            condition.parse_arguments(args='-')

        with self.assertRaises(ConditionParserError, msg='Check on setup with incorrect length failed'):
            condition.parse_arguments(args='-10')

        with self.assertRaises(ConditionParserError, msg='Check on setup with incorrect range failed'):
            condition.parse_arguments(args='100-10')

        arguments = condition.parse_arguments(args='10-100,10,')
        self.assertListEqual(arguments, [(10, 100), (10, 10)],
                             msg='Check on setup with separator in the end line failed')
