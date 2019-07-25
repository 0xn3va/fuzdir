from requests import Response

from src.filter.conditions.CodeCondition import CodeCondition
from src.filter.FilterError import FilterError
from src.filter.conditions.ContentLengthCondition import ContentLengthCondition
from src.filter.conditions.GrepCondition import GrepCondition


class Filter:
    handlers = {
        'code': CodeCondition,
        'length': ContentLengthCondition,
        'grep': GrepCondition
    }

    _conditions_separator = ';'
    _handler_separator = ':'
    _args_separator = '='
    _ignore_key = 'ignore'

    def __init__(self, conditions: str = ''):
        self._conditions = []

        if len(conditions) == 0:
            return

        for condition in conditions.split(self._conditions_separator):
            handler, _, condition_args = condition.partition(self._args_separator)
            if len(condition_args) < 1:
                raise FilterError('Invalid condition: %s' % (condition,))

            head, _, tail = handler.partition(self._handler_separator)
            ignore = (head == self._ignore_key)
            if ignore:
                handler = tail

            handler_name, _, handler_args = handler.partition(self._handler_separator)

            try:
                handler = self.handlers[handler_name]()
                handler.setup(condition_args, handler_args)
                self._conditions.append((ignore, handler))
            except KeyError:
                raise FilterError('Invalid conditions name: %s' % (handler_name,))

        self._conditions.sort(key=lambda c: c[-1].priority.value, reverse=True)

    def inspect(self, response: Response):
        if response is None:
            return False
        return True if len(self._conditions) == 0 else all(condition[0] != condition[1].match(response) for condition in self._conditions)
