from requests import Response

from src.filter.condition.condition import Condition
from src.filter.condition.condition_priority import ConditionPriority
from src.network.network_utils import NetworkUtils


class ContentLengthCondition(Condition):
    def __init__(self, area: str, args):
        super(ContentLengthCondition, self).__init__(ConditionPriority.medium, area, args)

    def match(self, response: Response):
        content_length = NetworkUtils.content_length(response)
        ranges = self._args
        return any(lower <= content_length <= upper for lower, upper in ranges)
