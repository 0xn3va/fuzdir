import json

from requests import Response

from src.network.network_utils import NetworkUtils
from src.output.report.report import Report
from src.output.report.utils.data_names import DataNames


class JSONReport(Report):
    _begin_format = '{\n%s'
    _json_format = ',\n%s'
    _end = '\n}'

    def __init__(self, filename: str, mode: str = 'w', encoding: str = None):
        super(JSONReport, self).__init__(filename, mode, encoding)
        self._is_empty = True

    def close(self):
        self._write(self._end)
        super(JSONReport, self).close()

    def write(self, response: Response):
        response_json = json.dumps({
            NetworkUtils.path(response): {
                DataNames.status_code: str(response.status_code),
                DataNames.content_length: str(NetworkUtils.content_length(response))
            }
        }, indent=4)
        response_json = '\n'.join(response_json.split('\n')[1:-1])
        self._write((self._begin_format if self._is_empty else self._json_format) % (response_json,), end='')
        self._is_empty = False
