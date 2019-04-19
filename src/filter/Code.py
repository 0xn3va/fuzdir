from requests import Response

from src.filter.Condition import Condition
from src.filter.FilterException import FilterException


class Code(Condition):
    _min_codes = 100
    _max_codes = 599

    def __init__(self):
        self._codes = []

    def setup(self, args: list):
        try:
            self._codes = []
            for arg in args:
                code = int(arg)
                if code < self._min_codes or code > self._max_codes:
                    raise FilterException('Invalid HTTP status code: %s' % (code, ))
                self._codes.append(code)
        except ValueError:
            raise FilterException('HTTP status code must be a number')

    def match(self, response: Response):
        return True if response.status_code in self._codes else False
