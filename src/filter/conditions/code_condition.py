from requests import Response

from src.filter.conditions.condition import Condition
from src.filter.filter_error import FilterError
from src.filter.conditions.condition_priority import ConditionPriority


class CodeCondition(Condition):
    _min_codes = 100
    _max_codes = 599

    def __init__(self):
        super(CodeCondition, self).__init__(ConditionPriority.high)
        self._codes = []

    def setup(self, condition_args: str, handler_args: str = ''):
        try:
            self._codes.clear()
            for arg in condition_args.strip(self._args_separator).split(self._args_separator):
                code = int(arg)
                if code < self._min_codes or code > self._max_codes:
                    raise FilterError('Invalid HTTP status code: %s' % (code,))
                self._codes.append(code)
        except ValueError:
            raise FilterError('HTTP status code must be a number')

    def match(self, response: Response):
        return True if response.status_code in self._codes else False
