from requests import Response

from src.network.network_utils import NetworkUtils
from src.output.report.report import Report
from src.output.report.report_components import ReportComponents


class PlainReport(Report):
    def __init__(self, components: list, filename: str, mode: str = 'w', encoding: str = None):
        super(PlainReport, self).__init__(components, filename, mode, encoding)
        self._write(f'{ReportComponents.status_code}\t{ReportComponents.content_length}\t{ReportComponents.path}')

    def write(self, response: Response):
        self._write(f'{response.status_code}\t{NetworkUtils.content_length(response)}\t{NetworkUtils.path(response)}')
