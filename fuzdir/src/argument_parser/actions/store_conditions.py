import argparse

from src.argument_parser.actions.condition_parser.condition_parser_error import ConditionParserError
from src.argument_parser.actions.condition_parser.implement.content_length_condition_parser import \
    ContentLengthConditionParser
from src.argument_parser.actions.condition_parser.implement.grep_condition_parser import GrepConditionParser
from src.argument_parser.actions.condition_parser.implement.status_code_condition_parser import \
    StatusCodeConditionParser
from src.argument_parser.argument_manager_error import ArgumentManagerError
from src.filter.filter_type import FilterType


class StoreConditions(argparse.Action):
    _parsers = {
        FilterType.status_code: StatusCodeConditionParser,
        FilterType.response_length: ContentLengthConditionParser,
        FilterType.grep: GrepConditionParser
    }
    _conditions_separator = ';'
    _handler_separator = ':'
    _args_separator = '='
    _ignore_key = 'ignore'

    def __call__(self, parser, namespace, values, option_string=None):
        conditions = []
        if values is not None:
            values = values.strip().strip(self._conditions_separator)
            for value in values.split(self._conditions_separator):
                value, separator, args = value.partition(self._args_separator)
                if not args:
                    raise ArgumentManagerError(f'Invalid filter condition: {value}{separator}')

                ignore = False
                if value.startswith(f'{self._ignore_key}{self._handler_separator}'):
                    _, _, value = value.partition(self._handler_separator)
                    ignore = True

                name, _, area = value.partition(self._handler_separator)

                try:
                    parser = self._parsers[name]()
                    args = parser.parse_arguments(args)
                    area = parser.parse_area(area)
                except KeyError:
                    raise ArgumentManagerError(f'Invalid filter condition name: {name}')
                except ConditionParserError as e:
                    raise ArgumentManagerError(str(e))

                conditions.append((ignore, name, area, args))

        setattr(namespace, self.dest, conditions)
