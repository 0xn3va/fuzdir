from src.argument_parser.actions.parsers.report.report_parser import ReportParser
from src.argument_parser.actions.parsers.report.report_parser_error import ReportParserError
from src.output.report.report_components import ReportComponents


class JsonReportParser(ReportParser):
    _components_list = [name for name in vars(ReportComponents).values()
                        if isinstance(name, str) and name[0] != '_' and name != ReportComponents.path]

    def parse_components(self, components: str):
        components_list = []
        if components:
            for component in components.strip(self._args_separator).split(self._args_separator):
                component = component.strip()
                if component not in self._components_list:
                    raise ReportParserError(f'Incorrect argument: {component} for JSON report')
                components_list.append(component)

        return components_list
