import re

from requests import Response

from src.filter.filter_error import FilterError
from src.filter.conditions.condition import Condition
from src.filter.conditions.condition_priority import ConditionPriority


class GrepCondition(Condition):
    def __init__(self):
        super(GrepCondition, self).__init__(ConditionPriority.low)
        self._grep_part = ''
        self._pattern = None
        self._parts_match = {
            'headers': self._headers_match,
            'body': self._body_match
        }

    def setup(self, condition_args: str, handler_args: str = ''):
        if len(handler_args) > 0 and handler_args not in self._parts_match:
            raise FilterError('Invalid arguments: %s' % (handler_args,))
        self._grep_part = handler_args
        try:
            self._pattern = re.compile(condition_args)
        except re.error:
            raise FilterError('Invalid pattern %s' % (condition_args,))

    def match(self, response: Response):
        if len(self._grep_part) > 0:
            return self._parts_match[self._grep_part]
        return any(part_match(response) for part_match in self._parts_match.values())

    def _headers_match(self, response: Response):
        return self._pattern.search('\r\n'.join('%s: %s' % (k, v,) for k, v in response.headers.items())) is not None

    def _body_match(self, response: Response):
        return self._pattern.search(response.text) is not None
