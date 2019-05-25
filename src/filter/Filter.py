from requests import Response

from src.filter.conditions.Code import Code
from src.filter.FilterError import FilterError
from src.filter.conditions.ContentLength import ContentLength
from src.filter.conditions.Grep import Grep


class Filter:
    handlers = {
        'code': Code,
        'length': ContentLength,
        'grep': Grep
    }

    _conditions_separator = ';'
    _handler_separator = ':'
    _args_separator = '='
    _invert_key = 'invert'

    def __init__(self, conditions: str = ''):
        self._conditions = []

        if len(conditions) == 0:
            return

        # -x invert:code=200,301 : filter key
        # -x code=200,301 : filter key
        # -v : invert key (dep)

        # -x handler=args - condition

        for condition in conditions.split(self._conditions_separator):
            handler, _, condition_args = condition.partition(self._args_separator)
            if len(condition_args) < 1:
                raise FilterError('Invalid condition: %s' % (condition,))

            head, _, tail = handler.partition(self._handler_separator)
            invert = (head == self._invert_key)
            if invert:
                handler = tail

            handler_name, _, handler_args = handler.partition(self._handler_separator)

            try:
                handler = self.handlers[handler_name]()
                handler.setup(condition_args, handler_args)
                self._conditions.append((invert, handler))
            except KeyError:
                raise FilterError('Invalid conditions name: %s' % (handler_name,))

        self._conditions.sort(key=lambda c: c[-1].priority.value, reverse=True)

    def inspect(self, response: Response):
        if response is None:
            return False
        return True if len(self._conditions) == 0 else any(condition[0] != condition[1].match(response) for condition in self._conditions)
