import uuid
from enum import Enum

from django.db import models

from src.common.models import BaseModel


class ProcessingStatus(Enum):
    PENDING = "PENDING"
    COMPLETED = "COMPLETED"

    @classmethod
    def choices(cls):
        return tuple((i.name, i.value) for i in cls)


class Video(models.Model):
    id: models.UUIDField = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )
    title: models.CharField = models.CharField(max_length=100)
    file = models.FileField(upload_to="raw", null=True, blank=True)
    status: models.CharField = models.CharField(
        max_length=10,
        default=ProcessingStatus.PENDING.value,
        choices=ProcessingStatus.choices(),
    )
    log_file = models.FileField(null=True, blank=True)

    def __str__(self):
        return f"{self.title} - {self.status}"


class Subtitle(BaseModel):
    video: models.ForeignKey = models.ForeignKey(Video, on_delete=models.CASCADE)

    sequence: models.IntegerField = models.IntegerField()
    language: models.CharField = models.CharField(max_length=20)
    description: models.TextField = models.TextField()
    start_time: models.IntegerField = models.IntegerField(default=0)
    end_time: models.IntegerField = models.IntegerField(default=0)

    class Meta:
        ordering = ["sequence"]
