from abc import ABC, abstractmethod


class IEntityFetcher(ABC):
    @abstractmethod
    def fetch(self, **kwargs) -> list | dict:
        ...

    def update(self, **kwargs) -> dict:
        ...
