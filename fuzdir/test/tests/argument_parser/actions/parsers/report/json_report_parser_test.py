import unittest

from src.argument_parser.actions.parsers.report.implement.json_report_parser import JsonReportParser
from src.argument_parser.actions.parsers.report.report_parser_error import ReportParserError
from src.output.report.report_components import ReportComponents
from test.mocks.utils import random_string


class JsonReportParserTest(unittest.TestCase):
    def test_parse_components(self):
        condition = JsonReportParser()
        with self.assertRaises(ReportParserError, msg='Check on parse components with undefined report component failed'):
            condition.parse_components(components=random_string())

        with self.assertRaises(ReportParserError, msg='Check on parse components with path component failed'):
            condition.parse_components(components=ReportComponents.path)

        self.assertFalse(condition.parse_components(components=None), msg='Check on parse undefined components failed')

        components = [name for name in vars(ReportComponents).values()
                      if isinstance(name, str) and name[0] != '_' and name != ReportComponents.path]
        self.assertListEqual(components, condition.parse_components(components=', '.join(components)),
                             msg='Check on parse components with all defined report components with extra spaces and commas failed')
