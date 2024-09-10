import json
from typing import Iterable

from src.video_processor.dto.subtitles_dtos import (
    SubtitleChunk,
    Subtitles,
    TimeFrame,
    TimeStamp,
)


class SrtParser:
    __raw: str
    __processed_data: Subtitles

    def __init__(self, str_data: str):
        self.__raw = str_data.strip()
        self.__processed_data = self.__parse()

    def __parse(self):
        if not self.__raw:
            return Subtitles([])
        raw_chunks = self.__raw.split("\n\n")
        parsed_chunks: list[SubtitleChunk] = []

        for raw_chunk in raw_chunks:
            chunk_sections = filter(
                lambda val: val != "",
                map(lambda val: val.strip(), raw_chunk.strip().split("\n")),
            )
            parsed_chunks.append(self.__parse_raw_chunk(chunk_sections))

        return Subtitles(parsed_chunks)

    def __parse_raw_chunk(self, sequence: Iterable[str]) -> SubtitleChunk:
        iterator = iter(sequence)
        sequence_id = next(iterator)
        time_frame = next(iterator)
        subtitles = [*iterator]
        return SubtitleChunk(
            id=int(sequence_id),
            time_frame=self.__parse_time_frame(time_frame),
            subtitles=self.__parse_subtitles(subtitles),
        )

    def __parse_time_frame(self, time_frame: str) -> TimeFrame:
        start, end = time_frame.split(" --> ")
        return TimeFrame(
            start=self.__parse_timestamp(start),
            end=self.__parse_timestamp(end),
        )

    def __parse_timestamp(self, timestamp: str) -> TimeStamp:
        hours, minutes, seconds = timestamp.split(":")
        seconds, milliseconds = seconds.split(",")

        return TimeStamp(
            hrs=int(hours),
            mins=int(minutes),
            secs=int(seconds),
            millis=int(milliseconds),
        )

    def __parse_subtitles(self, subtitles: list[str]) -> str:
        return "\n".join(map(lambda x: x.strip(), subtitles))

    def raw_data(self) -> Subtitles:
        return self.__processed_data

    def to_json(self):
        return json.dumps(self.raw_data())
