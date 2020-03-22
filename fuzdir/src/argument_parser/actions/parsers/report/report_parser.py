from abc import ABC, abstractmethod


class ReportParser(ABC):
    _args_separator = ','

    @abstractmethod
    def parse_components(self, components: str):
        raise NotImplementedError
