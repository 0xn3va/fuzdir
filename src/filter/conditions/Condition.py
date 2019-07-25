from abc import ABC, abstractmethod

from requests import Response

from src.filter.conditions.ConditionPriority import ConditionPriority


class Condition(ABC):
    _args_separator = ','

    def __init__(self, priority: ConditionPriority):
        self.priority = priority

    @abstractmethod
    def setup(self, condition_args: str, handler_args: str = ''):
        return

    @abstractmethod
    def match(self, response: Response) -> bool:
        return False
