from src.argument_parser.actions.parsers.report.report_parser import ReportParser
from src.argument_parser.actions.parsers.report.report_parser_error import ReportParserError


class PlainReportParser(ReportParser):
    def parse_components(self, components: str):
        if components:
            raise ReportParserError('Plain text report does not support any components')
