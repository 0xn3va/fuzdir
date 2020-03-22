from json import dumps

from requests import Response

from src.network.network_utils import NetworkUtils
from src.output.report.report import Report
from src.output.report.report_components import ReportComponents


class JsonReport(Report):
    _default_components = [
        ReportComponents.status_code,
        ReportComponents.content_length
    ]
    _component_handlers = {
        ReportComponents.body: lambda response: response.text,
        ReportComponents.content_length: lambda response: str(NetworkUtils.content_length(response)),
        ReportComponents.headers: lambda response: response.headers,
        ReportComponents.status_code: lambda response: str(response.status_code)
    }

    def __init__(self, components: list, filename: str, mode: str = 'w', encoding: str = None):
        super(JsonReport, self).__init__(components or self._default_components, filename, mode, encoding)
        self._is_empty = True

    def close(self):
        self._write('}')
        super(JsonReport, self).close()

    def write(self, response: Response):
        components = {}
        for component in self._components:
            components[component] = self._component_handlers[component](response)
        response_json = dumps({NetworkUtils.path(response): components})[1: -1]
        if self._is_empty:
            self._write(f'{{{response_json}', end='')
        else:
            self._write(f', {response_json}', end='')
        self._is_empty = False
