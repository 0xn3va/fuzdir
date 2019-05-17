from abc import ABC, abstractmethod

from requests import Response

from src.filter.conditions.ConditionPriority import ConditionPriority


class Condition(ABC):
    args_separator = ','

    def __init__(self, priority: ConditionPriority):
        self._priority = priority

    @abstractmethod
    def setup(self, args: str):
        return

    @abstractmethod
    def match(self, response: Response) -> bool:
        return False