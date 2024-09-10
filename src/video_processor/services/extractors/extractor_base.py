from abc import ABC, abstractmethod

from src.video_processor.dto.subtitles_dtos import SubtitleSet


class ExtractorBase(ABC):
    @abstractmethod
    def extract_subtitle_sets(self, absolute_file_path: str) -> list[SubtitleSet]:
        pass
