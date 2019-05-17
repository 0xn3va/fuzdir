from abc import ABC, abstractmethod

from requests import Response


class Condition(ABC):
    args_separator = ','

    @abstractmethod
    def setup(self, args: str):
        return

    @abstractmethod
    def match(self, response: Response) -> bool:
        return False
