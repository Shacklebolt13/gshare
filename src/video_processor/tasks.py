import logging

from celery import shared_task

from src.video_processor.services.extractors.ffmpeg_extractor import FfmpegExtractor
from src.video_processor.services.subtitle_processor import SubtitleProcessor

from .models import ProcessingStatus, Video

logging = logging.getLogger(__name__)


@shared_task
def process_subtitles(video_id):
    logging.info(f"Recieved task request for video id : {video_id}")
    video_object = Video.objects.get(id=video_id)
    if not video_object:
        logging.fatal(f"Video not found for id : {video_id}")
        return
    extractor_instance = FfmpegExtractor()
    logging.info("Beginning to process Subtitles")
    SubtitleProcessor(
        video_object.file.file,
        extractor_instance,
    ).process_subtitles(video_object)
    logging.info("Updating video status")
    video_object.status = ProcessingStatus.COMPLETED.value
    video_object.save()
    logging.info("Completed processing subtitles")
