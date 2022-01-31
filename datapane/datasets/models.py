from __future__ import annotations

import csv
import pathlib

from datetime import datetime

from django.core.files import File
from django.db import models


class DataSet(models.Model):
    upload: File = models.FileField("CSV Upload", upload_to="uploads/%Y/%m/%d/")
    created: datetime = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return pathlib.Path(self.upload.name).name

    def csv_reader(self) -> csv.Reader:
        return csv.reader(self.upload.open("r"))
