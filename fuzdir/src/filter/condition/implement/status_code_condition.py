from requests import Response

from src.filter.condition.condition import Condition
from src.filter.condition.condition_priority import ConditionPriority


class StatusCodeCondition(Condition):
    def __init__(self, area: str, args):
        super(StatusCodeCondition, self).__init__(ConditionPriority.high, area, args)

    def match(self, response: Response) -> bool:
        status_code = response.status_code
        codes = self._args
        return any(lower <= status_code <= upper for lower, upper in codes)
