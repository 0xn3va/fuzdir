from requests import Response

from src.filter.Code import Code
from src.filter.FilterError import FilterError


class Filter:
    handlers = {
        'code': Code
    }

    def __init__(self, conditions: str = '', invert: bool = False):
        self._conditions = []
        self._invert = invert

        if len(conditions) == 0:
            return

        # -x code=200,301 : filter key
        # -v : invert key

        for condition in conditions.split(';'):
            name_args = condition.split('=')
            if len(name_args) != 2:
                raise FilterError('Invalid condition: %s' % (name_args,))
            name, args = name_args
            try:
                handler = self.handlers[name]()
                handler.setup(args.split(','))
                self._conditions.append(handler)
            except KeyError:
                raise FilterError('Invalid conditions name: %s' % (name,))

    def inspect(self, response: Response):
        if response is None:
            return False
        return True if len(self._conditions) == 0 else any(
            self._invert != condition.match(response) for condition in self._conditions)
