import re

from src.argument_parser.actions.parsers.condition.condition_parser import ConditionParser
from src.argument_parser.actions.parsers.condition.condition_parser_error import ConditionParserError
from src.filter.condition.implement.utils.grep_areas import GrepAreas


class GrepConditionParser(ConditionParser):
    _code_separator = '-'
    _min_code = 100
    _max_code = 599

    def parse_arguments(self, args: str):
        try:
            return re.compile(args)
        except re.error:
            raise ConditionParserError(f'Invalid pattern {args}')

    def parse_area(self, area: str):
        area = area.strip()
        if area and area not in (GrepAreas.headers, GrepAreas.body):
            raise ConditionParserError(f'Invalid filter condition area: {area}')

        return area
