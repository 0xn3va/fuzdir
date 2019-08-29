from requests import Response

from src.network.network_utils import NetworkUtils
from src.output.report.report import Report


class PlainReport(Report):
    _row_format = '%d\t%d\t%s'

    def write(self, response: Response):
        self._write(self._row_format % (response.status_code, NetworkUtils.content_length(response), response.url,))
