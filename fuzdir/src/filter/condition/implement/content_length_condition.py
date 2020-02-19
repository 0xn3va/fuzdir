from requests import Response

from src.filter.filter_error import FilterError
from src.filter.condition.condition import Condition
from src.filter.condition.condition_priority import ConditionPriority
from src.network.network_utils import NetworkUtils


class ContentLengthCondition(Condition):
    _length_separator = '-'

    def __init__(self):
        super(ContentLengthCondition, self).__init__(ConditionPriority.medium)
        self._ranges = []

    def setup(self, args: str, area: str):
        try:
            self._ranges.clear()
            for arg in args.strip(self._args_separator).split(self._args_separator):
                lengths = [length for length in map(int, arg.split(self._length_separator))]
                if len(lengths) > 1:
                    lower, upper = lengths
                    if upper < lower:
                        raise FilterError(f'Invalid content length range {args}')
                    self._ranges.append((lower, upper))
                else:
                    self._ranges.append((lengths[0], lengths[0]))
        except ValueError:
            raise FilterError(f'Incorrect content length {args}')

    def match(self, response: Response):
        content_length = NetworkUtils.content_length(response)
        return any(lower <= content_length <= upper for lower, upper in self._ranges)
