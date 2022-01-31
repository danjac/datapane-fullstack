from __future__ import annotations

from datetime import datetime

from django.core.files import File
from django.db import models


class DataSet(models.Model):
    upload: File = models.FileField("CSV Upload", upload_to="uploads/%Y/%m/%d/")

    # NOTE: setting size as a separate field rather than using upload.size
    # makes it easier in future to query/order datasets with a "size" filter.
    size: int = models.PositiveIntegerField()

    created: datetime = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.upload.name

    def save(self, **kwargs):
        self.size = self.upload.size
        super().save(**kwargs)
