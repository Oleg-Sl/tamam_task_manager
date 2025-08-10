from abc import ABC, abstractmethod
from typing import Union


class IEntityFetcher(ABC):
    @abstractmethod
    def fetch(self, **kwargs) -> Union[list, dict]:
        ...

    def update(self, **kwargs) -> dict:
        ...
