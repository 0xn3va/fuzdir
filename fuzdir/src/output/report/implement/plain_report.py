from requests import Response

from src.network.network_utils import NetworkUtils
from src.output.report.report import Report
from src.output.report.utils.data_names import DataNames


class PlainReport(Report):
    _header_format = '%s\t%s\t%s'
    _row_format = '%d\t%d\t%s'

    def __init__(self, filename: str, mode: str = 'w', encoding: str = None):
        super(PlainReport, self).__init__(filename, mode, encoding)
        self._write(self._header_format % (DataNames.status_code, DataNames.content_length, DataNames.path))

    def write(self, response: Response):
        self._write(self._row_format %
                    (response.status_code, NetworkUtils.content_length(response), NetworkUtils.path(response),))
