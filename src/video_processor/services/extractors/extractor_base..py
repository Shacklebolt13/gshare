from abc import ABC, abstractmethod


class ExtractorBase(ABC):

    @abstractmethod
    def extract_subtitle_set(self, filename: str) -> list[dict]:
        pass
