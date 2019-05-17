from src.filter.FilterError import FilterError
from src.filter.conditions.Condition import Condition
from src.filter.conditions.ConditionPriority import ConditionPriority
from src.network.Response import Response
from src.network.utils import NetworkUtil


class ContentLength(Condition):
    _length_separator = '-'

    def __init__(self):
        super(ContentLength, self).__init__(ConditionPriority.medium)
        self._ranges = []

    def setup(self, args: str):
        try:
            for arg in args.split(self.args_separator):
                lengths = [length for length in map(int, arg.split(self._length_separator))]
                if len(lengths) > 2 or any(length < 0 for length in lengths):
                    raise FilterError('Invalid content length range %s' % (args,))
                self._ranges.append(lengths)
        except ValueError:
            raise FilterError('Incorrect content length %s' % (args,))

    def match(self, response: Response):
        def _match(length_range, content_length):
            if len(length_range) > 1:
                mn, mx = length_range
                return mn <= content_length <= mx
            else:
                return length_range[0] == content_length

        return all(_match(length_range, NetworkUtil.content_length(response)) for length_range in self._ranges)
