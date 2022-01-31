from django import forms

from datapane.datasets.models import DataSet


class DataSetForm(forms.ModelForm):
    class Meta:
        model = DataSet
        fields = ("upload",)
