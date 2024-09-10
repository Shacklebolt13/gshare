import logging
import uuid

from celery import shared_task
from django.conf import settings

from config.settings import BASE_DIR, MEDIA_ROOT
from src.video_processor.services.extractors.ffmpeg_extractor import FfmpegExtractor
from src.video_processor.services.subtitle_processor import SubtitleProcessor

from .models import ProcessingStatus, Video


@shared_task
def process_subtitles(video_id: uuid.UUID):
    logger = logging.getLogger(f"task-{video_id}")
    log_filename = settings.MEDIA_ROOT / f"logs/{video_id}.log"
    logger.setLevel(logging.INFO)
    file_handler = logging.FileHandler(log_filename)
    logger.addHandler(file_handler)

    logger.info(f"Recieved task request for video id : {video_id}")
    video_object = Video.objects.get(id=video_id)
    if not video_object:
        logging.error(f"Video not found for id : {video_id}")
        return
    extractor_instance = FfmpegExtractor(str(video_id))
    logger.info("Beginning to process Subtitles")
    SubtitleProcessor(
        video_object,
        extractor_instance,
    ).process_subtitles(video_object.id)
    logger.info("Updating video status")
    video_object.status = ProcessingStatus.COMPLETED.value
    video_object.log_file = log_filename
    video_object.save()
    logger.info("Completed processing subtitles")
