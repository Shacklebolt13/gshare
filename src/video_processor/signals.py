from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from .models import ProcessingStatus, Video
from .tasks import cleanup_files, process_subtitles


@receiver(post_save, sender=Video)
def submit_subtitle_extraction_task(sender, instance: Video, created, **kwargs):
    if created or instance.status == ProcessingStatus.PENDING.value:
        task = process_subtitles.delay(instance.id)  # type: ignore
        print(f"Task {task.id} submitted for video {instance.id}")
    else:
        print("No task submitted")


@receiver(post_delete, sender=Video)
def delete_video_files(sender, instance: Video, **kwargs):
    cleanup_files.delay(instance.file.path, instance.log_file.path)  # type: ignore
