import uuid

from django.db import models

from src.common.models import BaseModel


# Create your models here.
class Video(models.Model):
    id: models.UUIDField = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )
    job: models.ForeignKey = models.ForeignKey("files.Job", on_delete=models.PROTECT)


class Subtitle(BaseModel):
    video: models.ForeignKey = models.ForeignKey(Video, on_delete=models.CASCADE)
    log_file = models.FileField()

    sequence: models.IntegerField = models.IntegerField()
    language: models.CharField = models.CharField(max_length=20)
    description: models.TextField = models.TextField()
    start_time: models.IntegerField = models.IntegerField(default=0)
    end_time: models.IntegerField = models.IntegerField(default=0)
