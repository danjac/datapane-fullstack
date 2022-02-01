import csv
import mimetypes

from django import forms
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import UploadedFile

from datapane.datasets.models import DataSet

sniffer = csv.Sniffer()


class EntryForm(forms.Form):

    # NOTE: if we were doing actual signup/login this would probably
    # inherit from auth UserCreationForm.

    name = forms.CharField(max_length=100)
    age = forms.IntegerField()
    email = forms.EmailField()


class DataSetForm(forms.ModelForm):
    class Meta:
        model = DataSet
        fields = ("upload",)

    def clean_upload(self) -> UploadedFile:

        # NOTE: assumption here is that max upload size is checked
        # in nginx/CloudFlare/etc and Django's DATA_UPLOAD_MAX_MEMORY_SIZE.
        # we might wish to set a specific upload size however for CSVs
        # either here or the Content-Length header in API endpoint.

        value = self.cleaned_data["upload"]

        # preliminary check: filename
        file_type, _ = mimetypes.guess_type(value.name)

        if file_type != "text/csv":
            raise ValidationError("Uploaded file must have text/csv type")

        # CSV sniffer check
        try:
            sniffer.sniff(value.readline().decode())
        except csv.Error:
            raise ValidationError("Uploaded CSV could not be read")

        value.seek(0)
        return value
