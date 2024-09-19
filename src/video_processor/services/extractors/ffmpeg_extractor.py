import json
import logging
import subprocess

from src.video_processor.dto.subtitles_dtos import Subtitles, SubtitleSet
from src.video_processor.services.extractors.extractor_base import ExtractorBase
from src.video_processor.services.parsers import srt_parser

LIST_STREAMS_COMMAND: str = "ffprobe -v error -show_streams -of json {filename}"

EXTRACT_STREAM_COMMAND: str = (
    "ffmpeg -loglevel info -i {filename} -map 0:s:{stream_id} -c copy -f srt -"
)


class FfmpegExtractor(ExtractorBase):

    __logger: logging.Logger

    def __init__(self, video_id: str):
        self.__logger = logging.getLogger(f"task-{video_id}")

    def get_streams(self, absolute_file_path: str) -> dict:
        self.__logger.info(f"fetching streams embedded into {absolute_file_path}")
        command = LIST_STREAMS_COMMAND.format(filename=absolute_file_path)
        result = subprocess.run(command, shell=True, stdout=subprocess.PIPE)
        result.stdout.decode("utf-8")
        self.__logger.debug(
            "found stream data, %s", result.stdout.replace(b"\n", b"\\n")
        )
        data = json.loads(result.stdout)
        return data

    def extract_stream(self, absolute_file_path: str, stream_id: int) -> Subtitles:
        self.__logger.info(f"Extracting stream by index {stream_id}")
        command = EXTRACT_STREAM_COMMAND.format(
            filename=absolute_file_path, stream_id=stream_id
        )
        result = subprocess.run(command, shell=True, stdout=subprocess.PIPE)
        self.__logger.debug(
            "found subtitles in stream 1 %s", result.stdout.replace(b"\n", b"\\n")
        )
        if result.stderr:
            self.__logger.warning(
                "found errors while processing ", result.stderr.replace(b"\n", b"\\n")
            )
        return srt_parser.SrtParser(result.stdout.decode("utf-8")).raw_data()

    def extract_subtitle_sets(self, absolute_file_path: str) -> list[SubtitleSet]:
        streams = self.get_streams(absolute_file_path)
        stream_count = len(streams.get("streams", []))
        self.__logger.info("found %s streams", stream_count)
        return [
            SubtitleSet(
                language=f"Language {i}",
                subtitles=self.extract_stream(absolute_file_path, i),
            )
            for i in range(stream_count)
        ]
