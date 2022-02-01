from __future__ import annotations

from django.core.paginator import InvalidPage, Paginator
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse
from django.views.decorators.http import require_http_methods

from datapane.datasets.forms import DataSetForm
from datapane.datasets.models import DataSet


@require_http_methods(["GET", "POST"])
def upload(request: HttpRequest) -> HttpResponse:

    if request.method == "GET":
        return TemplateResponse(request, "upload.html", {"form": DataSetForm()})

    form = DataSetForm(request.POST, request.FILES)

    context = {"form": form}

    if form.is_valid():

        dataset = form.save()

        context = {"form": DataSetForm(), **get_datarows_context(dataset, 1)}

    return TemplateResponse(request, "_upload.html", context)


@require_http_methods(["GET"])
def datarows(request: HttpRequest, dataset_id: int, page: int) -> HttpResponse:

    return TemplateResponse(
        request,
        "_datarows.html",
        get_datarows_context(get_object_or_404(DataSet, pk=dataset_id), page),
    )


def get_datarows_context(dataset: DataSet, page: int, per_page: int = 20) -> dict:

    reader = dataset.csv_reader()

    try:
        headers = next(reader)
        page_obj = Paginator(list(reader), per_page=per_page).page(page)
    except (StopIteration, InvalidPage):
        headers = []
        page_obj = None

    return {
        "dataset": dataset,
        "headers": headers,
        "page_obj": page_obj,
    }
