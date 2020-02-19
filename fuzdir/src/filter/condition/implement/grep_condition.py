import re

from requests import Response

from src.filter.condition.implement.utils.grep_areas import GrepAreas
from src.filter.filter_error import FilterError
from src.filter.condition.condition import Condition
from src.filter.condition.condition_priority import ConditionPriority


class GrepCondition(Condition):
    def __init__(self):
        super(GrepCondition, self).__init__(ConditionPriority.low)
        self._area = ''
        self._pattern = None
        self._handler = None

    def setup(self, args: str, area: str):
        if area:
            if area == GrepAreas.headers:
                self._handler = self._headers_match
            elif area == GrepAreas.body:
                self._handler = self._body_match
            else:
                raise FilterError(f'Invalid area: {area}')

        try:
            self._pattern = re.compile(args)
        except re.error:
            raise FilterError(f'Invalid pattern {args}')

    def match(self, response: Response) -> bool:
        handler = self._handler
        return handler(response) if handler else self._headers_match(response) or self._body_match(response)

    def _headers_match(self, response: Response):
        return self._pattern.search('\r\n'.join(f'{k}: {v}' for k, v in response.headers.items())) is not None

    def _body_match(self, response: Response):
        return self._pattern.search(response.text) is not None
