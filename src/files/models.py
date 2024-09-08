import uuid
from enum import Enum

from django.conf import settings
from django.db import models

from src.common import models as common_models


class JobStatus(Enum):
    PENDING = "Pending"
    COMPLETED = "Completed"

    @classmethod
    def choices(cls):
        return tuple((i.name, i.value) for i in cls)


class Job(common_models.BaseModel):
    id: models.UUIDField = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )
    title: models.CharField = models.CharField(max_length=100)
    file = models.FileField(upload_to="raw", null=True, blank=True)
    status: models.CharField = models.CharField(
        max_length=10, default="Pending", choices=JobStatus.choices()
    )

    def __str__(self):
        return f"{self.id}:{self.updated_at}:{self.status}"
