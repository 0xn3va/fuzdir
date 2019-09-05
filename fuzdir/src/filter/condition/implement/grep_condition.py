import re

from requests import Response

from src.filter.filter_error import FilterError
from src.filter.condition.condition import Condition
from src.filter.condition.condition_priority import ConditionPriority


class GrepCondition(Condition):
    def __init__(self):
        super(GrepCondition, self).__init__(ConditionPriority.low)
        self._area = ''
        self._pattern = None
        self._handlers = {
            'headers': self._headers_match,
            'body': self._body_match
        }

    def setup(self, args: str, area: str):
        if area and area not in self._handlers:
            raise FilterError('Invalid area: %s' % (area,))
        self._area = area
        try:
            self._pattern = re.compile(args)
        except re.error:
            raise FilterError('Invalid pattern %s' % (args,))

    def match(self, response: Response) -> bool:
        if self._area:
            return self._handlers[self._area](response)
        return any(match(response) for match in self._handlers.values())

    def _headers_match(self, response: Response):
        return self._pattern.search('\r\n'.join('%s: %s' % (k, v,) for k, v in response.headers.items())) is not None

    def _body_match(self, response: Response):
        return self._pattern.search(response.text) is not None
