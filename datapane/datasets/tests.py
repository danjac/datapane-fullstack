import http
import pathlib

from django.conf import settings
from django.core.files.base import ContentFile
from django.test import TestCase, override_settings
from django.urls import reverse, reverse_lazy

from datapane.datasets.models import DataSet

TEST_MEDIA_ROOT = settings.BASE_DIR / "test_media"


@override_settings(MEDIA_ROOT=TEST_MEDIA_ROOT)
def create_dataset(filename="test.csv"):
    # NOTE: in a larger project, this it would be easier to generate
    # factories with factory-boy or similar.
    dataset = DataSet()
    dataset.upload.save(filename, get_content_file(filename))
    dataset.save()
    return dataset


def get_content_file(filename, name=None):
    with (pathlib.Path(__file__).parent / filename).open("rb") as fp:
        return ContentFile(fp.read(), name=name)


class TestDataSetModel(TestCase):
    @override_settings(MEDIA_ROOT=TEST_MEDIA_ROOT)
    def test_csv_reader(self):
        dataset = create_dataset()
        reader = dataset.csv_reader()
        rows = list(reader)
        self.assertEqual(len(rows), 11)


class TestUploadView(TestCase):
    url = reverse_lazy("upload")

    def test_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, http.HTTPStatus.OK)
        self.assertTemplateUsed(response, "upload.html")

    def test_post_invalid(self):
        response = self.client.post(self.url, {})
        self.assertEqual(response.status_code, http.HTTPStatus.OK)
        self.assertTemplateUsed(response, "_upload.html")
        self.assertEqual(DataSet.objects.count(), 0)

    @override_settings(MEDIA_ROOT=TEST_MEDIA_ROOT)
    def test_post_invalid_csv(self):
        response = self.client.post(
            self.url, {"upload": get_content_file("empty.csv", "empty.csv")}
        )
        self.assertEqual(response.status_code, http.HTTPStatus.OK)
        self.assertTemplateUsed(response, "_upload.html")

    @override_settings(MEDIA_ROOT=TEST_MEDIA_ROOT)
    def test_post_valid(self):
        response = self.client.post(
            self.url, {"upload": get_content_file("test.csv", "test.csv")}
        )
        self.assertEqual(response.status_code, http.HTTPStatus.OK)
        self.assertTemplateUsed(response, "_upload.html")


class DataRowsView(TestCase):
    @override_settings(MEDIA_ROOT=TEST_MEDIA_ROOT)
    def test_get(self):
        dataset = create_dataset()
        response = self.client.get(reverse("datarows", args=[dataset.id, 1]))
        self.assertEqual(response.status_code, http.HTTPStatus.OK)

    @override_settings(MEDIA_ROOT=TEST_MEDIA_ROOT)
    def test_get_empty(self):
        dataset = create_dataset("empty.csv")
        response = self.client.get(reverse("datarows", args=[dataset.id, 1]))
        self.assertEqual(response.status_code, http.HTTPStatus.OK)
