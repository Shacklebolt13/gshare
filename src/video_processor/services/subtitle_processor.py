import logging
import uuid
from dataclasses import asdict

from src.common import utils
from src.video_processor.dto.subtitles_dtos import SubtitleSet
from src.video_processor.models import Subtitle, Video
from src.video_processor.services.extractors.extractor_base import ExtractorBase


class SubtitleProcessor:

    __file_path: str
    __extractor: ExtractorBase
    __logger: logging.Logger

    def __init__(self, video: Video, extractor: ExtractorBase):
        self.__file_path = video.file.file
        self.__extractor = extractor
        self.__logger = (
            logging.getLogger(f"task-{video.id}")
            if utils.is_celey_context()
            else logging.getLogger(__name__)
        )

    def __extract_subtitle_sets(self) -> list[SubtitleSet]:
        return self.__extractor.extract_subtitle_sets(self.__file_path)

    def __save_subtitles(self, video_id: uuid.UUID, subtitleSet: SubtitleSet):
        Subtitle.objects.bulk_create(
            (
                Subtitle(
                    video_id=video_id,
                    sequence=chunk.id,
                    language=subtitleSet.language,
                    start_time=chunk.time_frame.start.total_millis,
                    end_time=chunk.time_frame.end.total_millis,
                    description=chunk.subtitles,
                )
                for chunk in subtitleSet.subtitles.chunks
            )
        )

    def process_subtitles(self, video_id: uuid.UUID):
        subtitle_sets = self.__extract_subtitle_sets()
        for subtitle_set in subtitle_sets:
            self.__logger.debug("saving subtitle set: %s", asdict(subtitle_set))
            self.__save_subtitles(video_id, subtitle_set)
