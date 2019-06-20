from requests import Response

from src.filter.FilterError import FilterError
from src.filter.conditions.Condition import Condition
from src.filter.ConditionPriority import ConditionPriority
from src.network.NetworkUtils import NetworkUtils


class ContentLength(Condition):
    _length_separator = '-'

    def __init__(self):
        super(ContentLength, self).__init__(ConditionPriority.medium)
        self._ranges = []

    def setup(self, condition_args: str, handler_args: str = ''):
        try:
            for arg in condition_args.split(self._args_separator):
                lengths = [length for length in map(int, arg.split(self._length_separator))]
                if len(lengths) > 2 or any(length < 0 for length in lengths):
                    raise FilterError('Invalid content length range %s' % (condition_args,))
                self._ranges.append(lengths)
        except ValueError:
            raise FilterError('Incorrect content length %s' % (condition_args,))

    def match(self, response: Response):
        def _match(length_range, content_length):
            if len(length_range) > 1:
                mn, mx = length_range
                return mn <= content_length <= mx
            else:
                return length_range[0] == content_length

        return all(_match(length_range, NetworkUtils.content_length(response)) for length_range in self._ranges)
