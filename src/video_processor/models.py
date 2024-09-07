from django.db import models

from src.common.models import BaseModel


# Create your models here.
class Video(models.Model):
    job = models.ForeignKey("files.Job", on_delete=models.PROTECT)


class Subtitle(BaseModel):

    video = models.ForeignKey(Video, on_delete=models.CASCADE)

    sequence = models.IntegerField()
    language = models.CharField(max_length=20)
    description = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
