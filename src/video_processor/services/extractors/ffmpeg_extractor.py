import json
import logging
import subprocess
from fileinput import filename
from sys import stdout

from parsers import srt_parser

from src.video_processor.dto.subtitles_dtos import Subtitles, SubtitleSet
from src.video_processor.services.extractors.extractor_base import ExtractorBase

LIST_STREAMS_COMMAND: str = (
    "ffprobe -v error -show_entries stream=index,codec_type -of json {filename}"
)

EXTRACT_STREAM_COMMAND: str = (
    "ffmpeg -i {filename} -map 0:s:{stream_id} -c copy -f srt -"
)

logger = logging.getLogger(__name__)


class FfmpegExtractor(ExtractorBase):

    def get_streams(self, absolute_file_path: str) -> dict:
        logger.debug(f"fetching streams embedded into {absolute_file_path}")
        command = LIST_STREAMS_COMMAND.format(filename=absolute_file_path)
        result = subprocess.run(command, shell=True, stdout=subprocess.PIPE)
        result.stdout.decode("utf-8")
        logger.debug("found stream data, {}", result.stdout.replace(b"\n", b"\\n"))
        data = json.loads(result.stdout)
        return data

    def extract_stream(self, absolute_file_path: str, stream_id: int) -> Subtitles:
        logger.info(f"Extracting stream by index {stream_id}")
        command = EXTRACT_STREAM_COMMAND.format(
            filename=absolute_file_path, stream_id=stream_id
        )
        result = subprocess.run(command, shell=True, stdout=subprocess.PIPE)
        logging.debug(
            "found subtitles in stream 1 {}", result.stdout.replace(b"\n", b"\\n")
        )
        if stdout.errors:
            logging.debug(
                "found errors while processing ", result.stderr.replace(b"\n", b"\\n")
            )
        return srt_parser.SrtParser(result.stdout.decode("utf-8")).raw_data()

    def extract_subtitle_sets(self, absolute_file_path: str) -> list[SubtitleSet]:
        streams = self.get_streams(absolute_file_path)
        stream_count = len(streams.get("streams", []))
        logging.info("found {} streams", stream_count)
        return [
            SubtitleSet(
                language=f"Language {i}",
                subtitles=self.extract_stream(absolute_file_path, i),
            )
            for i in range(stream_count)
        ]
