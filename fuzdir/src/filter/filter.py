from requests import Response

from src.filter.condition.implement.status_code_condition import StatusCodeCondition
from src.filter.filter_error import FilterError
from src.filter.condition.implement.content_length_condition import ContentLengthCondition
from src.filter.condition.implement.grep_condition import GrepCondition


class Filter:
    _handlers = {
        'code': StatusCodeCondition,
        'length': ContentLengthCondition,
        'grep': GrepCondition
    }
    _conditions_separator = ';'
    _handler_separator = ':'
    _args_separator = '='
    _ignore_key = 'ignore'

    def __init__(self, conditions: str):
        self._conditions = []
        if not conditions:
            return

        for condition in conditions.strip(self._conditions_separator).split(self._conditions_separator):
            head, _, args = condition.partition(self._args_separator)
            if not args:
                raise FilterError(f'Invalid condition: {condition}')

            key, _, tail = head.partition(self._handler_separator)
            ignore = (key == self._ignore_key)
            if ignore:
                head = tail

            name, _, area = head.partition(self._handler_separator)

            try:
                handler = self._handlers[name]()
                handler.setup(args, area)
                self._conditions.append((ignore, handler))
            except KeyError:
                raise FilterError(f'Invalid condition name: {name}')

        self._conditions.sort(key=lambda c: c[-1].priority.value, reverse=True)

    def inspect(self, response: Response) -> bool:
        if not self._conditions:
            return True

        if response is None:
            return False

        return all(ignore ^ condition.match(response) for ignore, condition in self._conditions)
