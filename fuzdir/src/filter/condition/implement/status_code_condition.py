from requests import Response

from src.filter.condition.condition import Condition
from src.filter.filter_error import FilterError
from src.filter.condition.condition_priority import ConditionPriority


class StatusCodeCondition(Condition):
    _code_separator = '-'
    _min_code = 100
    _max_code = 599

    def __init__(self):
        super(StatusCodeCondition, self).__init__(ConditionPriority.high)
        self._codes = []

    def setup(self, args: str, area: str):
        try:
            self._codes.clear()
            for arg in args.strip(self._args_separator).split(self._args_separator):
                codes = [code for code in map(int, arg.split(self._code_separator))]
                if len(codes) > 1:
                    lower, upper = codes
                    if upper < lower or lower < self._min_code or self._max_code < upper:
                        raise FilterError(f'Invalid HTTP status codes range: {args}')
                    self._codes.append((lower, upper))
                else:
                    code = codes[0]
                    if code < self._min_code or self._max_code < code:
                        raise FilterError(f'Invalid HTTP status code: {code}')
                    self._codes.append((codes[0], codes[0]))
        except ValueError:
            raise FilterError('HTTP status code must be a number')

    def match(self, response: Response) -> bool:
        status_code = response.status_code
        return any(lower <= status_code <= upper for lower, upper in self._codes)
