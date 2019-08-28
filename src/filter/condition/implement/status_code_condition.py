from requests import Response

from src.filter.condition.condition import Condition
from src.filter.filter_error import FilterError
from src.filter.condition.condition_priority import ConditionPriority


class StatusCodeCondition(Condition):
    _min_code = 100
    _max_code = 599

    def __init__(self):
        super(StatusCodeCondition, self).__init__(ConditionPriority.high)
        self._codes = []

    def setup(self, args: str, area: str):
        try:
            self._codes.clear()
            for arg in args.strip(self._args_separator).split(self._args_separator):
                code = int(arg)
                if code < self._min_code or self._max_code < code:
                    raise FilterError('Invalid HTTP status code: %s' % (code,))
                self._codes.append(code)
        except ValueError:
            raise FilterError('HTTP status code must be a number')

    def match(self, response: Response) -> bool:
        return response.status_code in self._codes
