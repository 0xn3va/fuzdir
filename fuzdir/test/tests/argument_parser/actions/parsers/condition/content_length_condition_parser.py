import unittest

from src.argument_parser.actions.parsers.condition.condition_parser_error import ConditionParserError
from src.argument_parser.actions.parsers.condition.implement.content_length_condition_parser import \
    ContentLengthConditionParser


class ContentLengthConditionParserTest(unittest.TestCase):
    def test_parse_arguments(self):
        condition = ContentLengthConditionParser()
        with self.assertRaises(ConditionParserError, msg='Check on parse arguments with empty line failed'):
            condition.parse_arguments(args='-')

        with self.assertRaises(ConditionParserError, msg='Check on parse arguments with incorrect length failed'):
            condition.parse_arguments(args='-10')

        with self.assertRaises(ConditionParserError, msg='Check on parse arguments with incorrect range failed'):
            condition.parse_arguments(args='100-10')

        arguments = condition.parse_arguments(args='10-100,10,')
        self.assertListEqual(arguments, [(10, 100), (10, 10)],
                             msg='Check on parse arguments with separator in the end line failed')

    def test_parse_area(self):
        condition = ContentLengthConditionParser()
        with self.assertRaises(ConditionParserError, msg='Check on parse area with non empty value failed'):
            condition.parse_area(area='body')
