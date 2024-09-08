from celery import shared_task

from .models import ProcessingStatus, Video


@shared_task
def extract_subtitles(video_id):
    video_object = Video.objects.get(id=video_id)
    video_object.status = ProcessingStatus.COMPLETED.value
    video_object.save()
