from requests import Response

from src.filter.Condition import Condition


class Code(Condition):
    _min_codes = 100
    _max_codes = 599

    def __init__(self):
        self._codes = []

    def setup(self, *args):
        try:
            self._codes = []
            for arg in args:
                code = int(arg)
                if code < self._min_codes or code > self._max_codes:
                    # todo('raise exception')
                    return
                self._codes.append(code)
        except ValueError:
            # todo('raise exception')
            return

    def match(self, response: Response):
        return True if response.status_code in self._codes else False
