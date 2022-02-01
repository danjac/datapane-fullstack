from __future__ import annotations

from django.core.paginator import InvalidPage, Page, Paginator
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse
from django.views.decorators.http import require_http_methods

from datapane.datasets.forms import DataSetForm, EntryForm
from datapane.datasets.models import DataSet


@require_http_methods(["GET"])
def entry_form(request: HttpRequest) -> HttpResponse:

    return TemplateResponse(
        request,
        "entry_form.html",
        {
            "form": EntryForm(),
            "page_obj": get_dataset_page(1),
        },
    )


@require_http_methods(["POST"])
def process_entry_form(request: HttpRequest) -> HttpResponse:
    # NOTE: as we're not doing any signup/login, this just validates and exits.

    form = EntryForm(request.POST)
    success = False

    if form.is_valid():
        # reset the form
        success = True
        form = EntryForm()

    return TemplateResponse(
        request, "_entry_form.html", {"form": form, "success": success}
    )


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
def datasets(request: HttpRequest, page: int) -> HttpResponse:
    return TemplateResponse(
        request, "_datasets.html", {"page_obj": get_dataset_page(page)}
    )


@require_http_methods(["GET"])
def dataset(request: HttpRequest, dataset_id: int) -> HttpResponse:
    dataset = get_object_or_404(DataSet, pk=dataset_id)
    return TemplateResponse(
        request,
        "dataset.html",
        get_datarows_context(dataset, 1),
    )


@require_http_methods(["GET"])
def datarows(request: HttpRequest, dataset_id: int, page: int) -> HttpResponse:

    return TemplateResponse(
        request,
        "_datarows.html",
        get_datarows_context(get_object_or_404(DataSet, pk=dataset_id), page),
    )


def get_dataset_page(page: int, per_page: int = 20) -> Page:

    return Paginator(
        DataSet.objects.order_by("-created"),
        per_page=per_page,
        allow_empty_first_page=True,
    ).page(page)


def get_datarows_context(dataset: DataSet, page: int, per_page: int = 20) -> dict:
    # NOTE: this function loads the whole CSV into a list. While this is OK for
    # smaller datasets this could result in OOM issues with a very large file.
    # We should therefore consider a lazy-loading wrapper that plays nicely
    # with pagination.

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
