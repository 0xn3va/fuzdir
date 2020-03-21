from src.argument_parser.actions.condition_parser.condition_parser import ConditionParser
from src.argument_parser.actions.condition_parser.condition_parser_error import ConditionParserError


class ContentLengthConditionParser(ConditionParser):
    _length_separator = '-'

    def parse_arguments(self, args: str):
        arguments = []
        for arg in args.strip(self._args_separator).split(self._args_separator):
            try:
                lengths = [length for length in map(int, arg.split(self._length_separator))]
            except ValueError:
                raise ConditionParserError(f'Incorrect content length {args}')

            if len(lengths) > 1:
                lower, upper = lengths
                if upper < lower:
                    raise ConditionParserError(f'Invalid content length range {args}')
                arguments.append((lower, upper))
            else:
                arguments.append((lengths[0], lengths[0]))

        return arguments
