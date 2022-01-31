"""datapane URL Configuration
"""
from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView

from datapane.datasets import views

urlpatterns = [
    path("", TemplateView.as_view(template_name="home.html"), name="home"),
    path("upload/", views.upload, name="upload"),
    path("datarows/<int:dataset_id>/<int:page>/", views.datarows, name="datarows"),
    path("admin/", admin.site.urls),
]
