import unittest

from src.argument_parser.actions.parsers.report.implement.plain_report_parser import PlainReportParser
from src.argument_parser.actions.parsers.report.report_parser_error import ReportParserError


class PlainReportParserTest(unittest.TestCase):
    def test_parse_components(self):
        condition = PlainReportParser()
        with self.assertRaises(ReportParserError, msg='Check on parse components with non empty value failed'):
            condition.parse_components(components='body')
