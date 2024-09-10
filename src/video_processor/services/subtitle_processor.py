import logging

from src.video_processor.dto.subtitles_dtos import SubtitleSet
from src.video_processor.models import Subtitle, Video
from src.video_processor.services.extractors.extractor_base import ExtractorBase

logger = logging.getLogger(__name__)


class SubtitleProcessor:

    __file_path: str
    __extractor: ExtractorBase

    def __init__(self, absolute_file_path, extractor: ExtractorBase):
        self.__file_path = absolute_file_path
        self.__extractor = extractor

    def __extract_subtitle_sets(self) -> list[SubtitleSet]:
        return self.__extractor.extract_subtitle_sets(self.__file_path)

    def __save_subtitles(self, video: Video, subtitleSet: SubtitleSet):
        try:
            Subtitle.objects.bulk_create(
                (
                    Subtitle(
                        video=video,
                        sequence=chunk.id,
                        language=subtitleSet.language,
                        start_time=chunk.time_frame.start,
                        end_time=chunk.time_frame.end,
                        description=chunk.subtitles,
                    )
                    for chunk in subtitleSet.subtitles.chunks
                )
            )
        except Exception as e:
            logger.error(f"Error saving subtitles for video {video.id}: {e}")

    def process_subtitles(self, video: Video):
        subtitle_sets = self.__extract_subtitle_sets()
        for subtitle_set in subtitle_sets:
            self.__save_subtitles(video, subtitle_set)
