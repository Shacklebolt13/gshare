from fileinput import filename
import os
import sys
import subprocess
import json
from .parsers import src_parser
from .extractor_base import ExtractorBase

LIST_STREAMS_COMMAND: str = (
    "ffprobe -v error -show_entries stream=index,codec_type -of json {filename}"
)

EXTRACT_STREAM_COMMAND: str = (
    "ffmpeg -i {filename} -map 0:s:{stream_id} -c copy -f srt -"
)

class FfmpegExtractor(ExtractorBase):

    def get_streams(self,filename: str) -> dict:
        command = LIST_STREAMS_COMMAND.format(filename=filename)
        result = subprocess.run(command, shell=True, stdout=subprocess.PIPE)
        result.stdout.decode("utf-8")
        data = json.loads(result.stdout)
        return data

    def extract_stream(self,filename: str, stream_id: int) -> list[dict]:
        command = EXTRACT_STREAM_COMMAND.format(filename=filename, stream_id=stream_id)
        result = subprocess.run(command, shell=True, stdout=subprocess.PIPE)
        return srt_parser.SrtParser(result.stdout.decode("utf-8")).to_dict()

    def extract_subtitle_set(self, filename: str) -> list[dict]:
        subtitle_set_list = []
        streams =self.get_streams()
        stream_count = len(streams.get("streams", []))
        return [self.extract_stream(filename,i) for i in range(self.count_streams(filename))]        
