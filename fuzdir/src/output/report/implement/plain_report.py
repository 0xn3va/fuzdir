from requests import Response

from src.network.network_utils import NetworkUtils
from src.output.report.report import Report
from src.output.report.utils.data_names import DataNames


class PlainReport(Report):
    def __init__(self, filename: str, mode: str = 'w', encoding: str = None):
        super(PlainReport, self).__init__(filename, mode, encoding)
        self._write(f'{DataNames.status_code}\t{DataNames.content_length}\t{DataNames.path}')

    def write(self, response: Response):
        self._write(f'{response.status_code}\t{NetworkUtils.content_length(response)}\t{NetworkUtils.path(response)}')
