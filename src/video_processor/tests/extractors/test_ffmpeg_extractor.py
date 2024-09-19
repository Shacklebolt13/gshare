import pytest
from django.test import TestCase

from src.video_processor import signals
from src.video_processor.models import Video
from src.video_processor.services.extractors import ffmpeg_extractor


class TestFFmpegExtractor(TestCase):

    video: Video
    FILE_PATH = "media/raw/test2.mp4"
    instance: ffmpeg_extractor.FfmpegExtractor

    @pytest.mark.django_db
    def setUp(self):
        signals.disconnect_signals()
        self.video = Video(title="test_video")
        self.video.file.name = self.FILE_PATH
        self.video.save()
        self.instance = ffmpeg_extractor.FfmpegExtractor(self.video.id)

    def test_extract_subtitles(self):
        subtitle_sets = self.instance.extract_subtitle_sets(self.FILE_PATH)
        self.assertIsNotNone(subtitle_sets)
        self.assertNotEqual(len(subtitle_sets), 0)
