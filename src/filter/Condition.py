from abc import ABC, abstractmethod

from requests import Response


class Condition(ABC):
    @abstractmethod
    def setup(self, *args):
        return

    @abstractmethod
    def match(self, response: Response) -> bool:
        return False
