import json

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
        sequences = self.__raw.split("\n\n")
        return Subtitles([self.__parse_sequence(x.split("\n")) for x in sequences])

    def __parse_sequence(self, sequence: list[str]) -> SubtitleChunk:
        print(sequence)
        sequence_id, time_frame = sequence[:2]
        subtitles = sequence[2:]
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
