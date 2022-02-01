"""datapane URL Configuration
"""
from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView

from datapane.datasets import views

urlpatterns = [
    path("", TemplateView.as_view(template_name="home.html"), name="home"),
    path("upload/", views.upload, name="upload"),
    path("entry-form/", views.entry_form, name="entry_form"),
    path("process-entry-form/", views.process_entry_form, name="process_entry_form"),
    path("dataset/<int:dataset_id>/", views.dataset, name="dataset"),
    path("datasets/<int:page>/", views.datasets, name="datasets"),
    path("datarows/<int:dataset_id>/<int:page>/", views.datarows, name="datarows"),
    path("admin/", admin.site.urls),
]
