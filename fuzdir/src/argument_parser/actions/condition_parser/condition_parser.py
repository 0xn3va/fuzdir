from abc import ABC, abstractmethod


class ConditionParser(ABC):
    _args_separator = ','

    @abstractmethod
    def parse_arguments(self, args: str):
        raise NotImplementedError

    def parse_area(self, area: str):
        return
