from __future__ import annotations

from django.core.paginator import Page, Paginator
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse
from django.views.decorators.http import require_http_methods

from datapane.datasets.forms import DataSetForm
from datapane.datasets.models import DataSet

PAGE_SIZE = 20


@require_http_methods(["GET", "POST"])
def upload(request: HttpRequest) -> HttpResponse:

    if request.method == "GET":
        return TemplateResponse(request, "upload.html", {"form": DataSetForm()})

    form = DataSetForm(request.POST, request.FILES)
    dataset: DataSet | None = None
    page_obj: Page | None = None
    headers: list[str] = []

    if form.is_valid():

        dataset = form.save()
        reader = dataset.csv_reader()
        headers = next(reader)

        page_obj = Paginator(list(reader), per_page=PAGE_SIZE).page(1)

        # reset form
        form = DataSetForm()

    return TemplateResponse(
        request,
        "_upload.html",
        {
            "form": form,
            "dataset": dataset,
            "headers": headers,
            "page_obj": page_obj,
        },
    )


@require_http_methods(["GET"])
def datarows(request: HttpRequest, dataset_id: int, page: int) -> HttpResponse:

    dataset = get_object_or_404(DataSet, pk=dataset_id)
    reader = dataset.csv_reader()
    headers = next(reader)

    page_obj = Paginator(list(reader), per_page=PAGE_SIZE).page(page)

    return TemplateResponse(
        request,
        "_datarows.html",
        {
            "dataset": dataset,
            "headers": headers,
            "page_obj": page_obj,
        },
    )
