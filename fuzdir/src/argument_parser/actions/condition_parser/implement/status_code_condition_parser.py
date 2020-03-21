from src.argument_parser.actions.condition_parser.condition_parser import ConditionParser
from src.argument_parser.actions.condition_parser.condition_parser_error import ConditionParserError


class StatusCodeConditionParser(ConditionParser):
    _code_separator = '-'
    _min_code = 100
    _max_code = 599

    def parse_arguments(self, args: str):
        arguments = []
        for arg in args.strip(self._args_separator).split(self._args_separator):
            try:
                codes = [code for code in map(int, arg.split(self._code_separator))]
            except ValueError:
                raise ConditionParserError('HTTP status code must be a number')

            if len(codes) > 1:
                lower, upper = codes
                if upper < lower or lower < self._min_code or self._max_code < upper:
                    raise ConditionParserError(f'Invalid HTTP status codes range: {args}')
                arguments.append((lower, upper))
            else:
                code = codes[0]
                if code < self._min_code or self._max_code < code:
                    raise ConditionParserError(f'Invalid HTTP status code: {code}')
                arguments.append((codes[0], codes[0]))

        return arguments
