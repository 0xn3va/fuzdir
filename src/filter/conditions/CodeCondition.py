from requests import Response

from src.filter.conditions.Condition import Condition
from src.filter.FilterError import FilterError
from src.filter.conditions.ConditionPriority import ConditionPriority


class CodeCondition(Condition):
    _min_codes = 100
    _max_codes = 599

    def __init__(self):
        super(CodeCondition, self).__init__(ConditionPriority.high)
        self._codes = []

    def setup(self, condition_args: str, handler_args: str = ''):
        try:
            self._codes = []
            for arg in condition_args.split(self._args_separator):
                code = int(arg)
                if code < self._min_codes or code > self._max_codes:
                    raise FilterError('Invalid HTTP status code: %s' % (code,))
                self._codes.append(code)
        except ValueError:
            raise FilterError('HTTP status code must be a number')

    def match(self, response: Response):
        return True if response.status_code in self._codes else False
