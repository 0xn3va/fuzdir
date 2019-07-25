from requests import Response

from src.network.NetworkUtils import NetworkUtils
from src.output.reports.Report import Report


class PlainReport(Report):
    _row_format = '%d\t%d\t%s'

    def write(self, response: Response):
        self._write(self._row_format % (response.status_code, NetworkUtils.content_length(response), response.url,))
