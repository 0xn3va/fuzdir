from abc import ABC, abstractmethod

from requests import Response

from src.filter.condition.condition_priority import ConditionPriority


class Condition(ABC):
    def __init__(self, priority: ConditionPriority, area: str, args):
        self.priority = priority
        self._area = area
        self._args = args

    @abstractmethod
    def match(self, response: Response) -> bool:
        return False
