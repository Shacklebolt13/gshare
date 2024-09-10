from dataclasses import dataclass


@dataclass(kw_only=True)
class TimeStamp:
    hrs: int
    mins: int
    secs: int
    millis: int


@dataclass(kw_only=True)
class TimeFrame:
    start: TimeStamp
    end: TimeStamp


@dataclass(kw_only=True)
class SubtitleChunk:
    id: int
    time_frame: TimeFrame
    subtitles: str


@dataclass
class Subtitles:
    chunks: list[SubtitleChunk]


@dataclass(kw_only=True)
class SubtitleSet:
    language: str
    subtitles: Subtitles
