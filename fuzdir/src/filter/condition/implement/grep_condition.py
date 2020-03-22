from requests import Response

from src.filter.condition.implement.utils.grep_areas import GrepAreas
from src.filter.condition.condition import Condition
from src.filter.condition.condition_priority import ConditionPriority


class GrepCondition(Condition):
    def __init__(self, area: str, args):
        super(GrepCondition, self).__init__(ConditionPriority.low, area, args)
        self._handler = None
        if area:
            if area == GrepAreas.headers:
                self._handler = self._headers_match
            else:
                self._handler = self._body_match

    def match(self, response: Response) -> bool:
        handler = self._handler
        return handler(response) if handler else self._headers_match(response) or self._body_match(response)

    def _headers_match(self, response: Response):
        pattern = self._args
        return pattern.search('\r\n'.join(f'{k}: {v}' for k, v in response.headers.items())) is not None

    def _body_match(self, response: Response):
        pattern = self._args
        return pattern.search(response.text) is not None
