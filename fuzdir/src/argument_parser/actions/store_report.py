import argparse

from src.argument_parser.actions.parsers.report.implement.json_report_parser import JsonReportParser
from src.argument_parser.actions.parsers.report.implement.plain_report_parser import PlainReportParser
from src.argument_parser.argument_manager_error import ArgumentManagerError
from src.output import ReportType
from src.utils.file_utils import FileUtils


class StoreReport(argparse.Action):
    _parsers = {
        ReportType.plain: PlainReportParser,
        ReportType.json: JsonReportParser
    }
    _components_separator = ':'
    _path_separator = '='

    def __call__(self, parser, namespace, values, option_string=None):
        values, _, path = values.partition(self._path_separator)
        path = path.strip()
        if not path:
            raise ArgumentManagerError('Missing report file path')

        if not FileUtils.is_writable(path):
            raise ArgumentManagerError(f'The file {path} does not writable')

        name, _, components = values.partition(self._components_separator)
        name = name.strip()

        try:
            parser = self._parsers[name]()
            components = parser.parse_components(components)
            setattr(namespace, self.dest, (name, path, components))
        except KeyError:
            raise ArgumentManagerError(f'Invalid report type: {name}')
