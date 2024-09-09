import os
import sys
import subprocess
import json


class SrtParser:
    __raw: str
    __processed_data: list[dict]

    def __init__(self, str_data: str):
        self.__raw = str_data.strip()
        self.__processed_data = self.__parse()

    def __parse(self):
        sequences = self.__raw.split("\n\n")
        return [self.__parse_sequence(x.split("\n")) for x in sequences]

    def __parse_sequence(self, sequence: list[str]) -> dict:
        print(sequence)
        sequence_id, time_frame = sequence[:2]
        subtitles = sequence[2:]
        return {
            "id": int(sequence_id),
            "time_frame": self.__parse_time_frame(time_frame),
            "subtitles": self.__parse_subtitles(subtitles),
        }

    def __parse_time_frame(self, time_frame: str) -> dict[str, dict[str, int]]:
        start, end = time_frame.split(" --> ")
        return {
            "start": self.__parse_timestamp(start),
            "end": self.__parse_timestamp(end),
        }

    def __parse_timestamp(self, timestamp: str) -> dict[str, int]:
        hours, minutes, seconds = timestamp.split(":")
        seconds, milliseconds = seconds.split(",")
        return {
            "hours": int(hours),
            "minutes": int(minutes),
            "seconds": int(seconds),
            "milliseconds": int(milliseconds),
        }

    def __parse_subtitles(self, subtitles: list[str]) -> str:
        return "\n".join(map(lambda x: x.strip(), subtitles))

    def to_dict(self) -> dict:
        return self.__processed_data

    def to_json(self):
        return json.dumps(self.to_dict())