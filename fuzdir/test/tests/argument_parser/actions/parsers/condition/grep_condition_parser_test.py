import unittest

from src.argument_parser.actions.parsers.condition.condition_parser_error import ConditionParserError
from src.argument_parser.actions.parsers.condition.implement.grep_condition_parser import GrepConditionParser
from src.filter.condition.implement.utils.grep_areas import GrepAreas


class GrepConditionParserTest(unittest.TestCase):
    def test_parse_arguments(self):
        condition = GrepConditionParser()
        with self.assertRaises(ConditionParserError, msg='Check on invalid pattern failed'):
            condition.parse_arguments(args='[')

    def test_parse_area(self):
        condition = GrepConditionParser()
        with self.assertRaises(ConditionParserError, msg='Check on invalid grep part failed'):
            condition.parse_area(area='test')

        self.assertEqual(GrepAreas.headers, condition.parse_area(area=f' {GrepAreas.headers} '),
                         msg='Check on strip extra spaces failed')
