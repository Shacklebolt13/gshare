from django.db import models

from src.common.models import BaseModel


# Create your models here.
class Video(models.Model):
    job: models.ForeignKey = models.ForeignKey("files.Job", on_delete=models.PROTECT)


class Subtitle(BaseModel):
    video: models.ForeignKey = models.ForeignKey(Video, on_delete=models.CASCADE)
    log_file = models.FileField()

    sequence: models.IntegerField = models.IntegerField()
    language: models.CharField = models.CharField(max_length=20)
    description: models.TextField = models.TextField()
    start_time: models.DateTimeField = models.DateTimeField()
    end_time: models.DateTimeField = models.DateTimeField()
