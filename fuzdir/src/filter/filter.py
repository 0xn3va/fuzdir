from requests import Response

from src.filter.condition.implement.status_code_condition import StatusCodeCondition
from src.filter.condition.implement.content_length_condition import ContentLengthCondition
from src.filter.condition.implement.grep_condition import GrepCondition
from src.filter.filter_type import FilterType


class Filter:
    _handlers = {
        FilterType.status_code: StatusCodeCondition,
        FilterType.response_length: ContentLengthCondition,
        FilterType.grep: GrepCondition
    }

    def __init__(self, conditions: list):
        self._conditions = []
        for condition in conditions:
            ignore, name, area, args = condition
            handler = self._handlers[name](area, args)
            self._conditions.append((ignore, handler))

        self._conditions.sort(key=lambda c: c[-1].priority.value, reverse=True)

    def inspect(self, response: Response) -> bool:
        if not self._conditions:
            return True

        if response is None:
            return False

        return all(ignore ^ condition.match(response) for ignore, condition in self._conditions)
