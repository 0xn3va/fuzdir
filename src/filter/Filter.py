from requests import Response

from src.filter.conditions.Code import Code
from src.filter.FilterError import FilterError
from src.filter.conditions.ContentLength import ContentLength


class Filter:
    handlers = {
        'code': Code,
        'length': ContentLength
    }

    _conditions_separator = ';'
    _name_separator = ':'
    _args_separator = '='
    _invert_key = 'invert'

    def __init__(self, conditions: str = ''):
        self._conditions = []

        if len(conditions) == 0:
            return

        # -x invert:code=200,301 : filter key
        # -x code=200,301 : filter key
        # -v : invert key (dep)

        for condition in conditions.split(self._conditions_separator):
            condition_name, _, args = condition.partition(self._args_separator)
            if len(args) < 1:
                raise FilterError('Invalid condition: %s' % (condition,))

            invert, _, name_args = condition_name.partition(self._name_separator)
            invert = (invert == self._invert_key)
            name = name_args if not invert else condition_name

            try:
                handler = self.handlers[name.split(self._name_separator)[0]]()
                handler.setup(args)
                # todo('Add conditions sort by priority')
                self._conditions.append((invert, handler))
            except KeyError:
                raise FilterError('Invalid conditions name: %s' % (name,))

    def inspect(self, response: Response):
        if response is None:
            return False
        return True if len(self._conditions) == 0 else any(condition[0] != condition[1].match(response) for condition in self._conditions)
