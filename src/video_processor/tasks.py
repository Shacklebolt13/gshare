import logging
import os
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
    relative_file_path = f"logs/{video_id}.log"
    log_filename = settings.MEDIA_ROOT / relative_file_path
    logger.setLevel(logging.INFO)
    file_handler = logging.FileHandler(log_filename)
    logger.addHandler(file_handler)

    logger.info(f"Recieved task request for video id : {video_id}")
    video_object = Video.objects.get(id=video_id)
    if not video_object:
        logger.error(f"Video not found for id : {video_id}")
        return
    try:
        extractor_instance = FfmpegExtractor(str(video_id))
        logger.info("Beginning to process Subtitles")
        SubtitleProcessor(
            video_object,
            extractor_instance,
        ).process_subtitles(video_object.id)
        logger.info("Updating video status")
        video_object.log_file.name = relative_file_path
    except Exception as e:
        logger.error("Error while processing subtitles", e)

    video_object.status = ProcessingStatus.COMPLETED.value
    video_object.save()
    logger.info("Completed processing subtitles")


@shared_task
def cleanup_files(video_file_absolute_path: str, log_file_absolute_path: str):
    logger = logging.getLogger("celery")
    logger.info(f"Cleaning up files for video : {video_file_absolute_path}")
    try:
        os.remove(video_file_absolute_path)
        os.remove(log_file_absolute_path)
        logger.info(f"Cleaned up files for video : {video_file_absolute_path}")
    except Exception as exception:
        logger.error("Error while cleaning up files : %s", exception)
