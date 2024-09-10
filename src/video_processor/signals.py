from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import ProcessingStatus, Video
from .tasks import process_subtitles


@receiver(post_save, sender=Video)
def submit_subtitle_extraction_task(sender, instance: Video, created, **kwargs):
    if created or instance.status == ProcessingStatus.PENDING.value:
        task = process_subtitles.delay(instance.id)  # type: ignore
        print(f"Task {task.id} submitted for video {instance.id}")
    else:
        print("No task submitted")
