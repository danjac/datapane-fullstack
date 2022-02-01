import http
import pathlib

from django.conf import settings
from django.core.files.base import ContentFile
from django.test import TestCase, override_settings
from django.urls import reverse_lazy

from datapane.datasets.models import DataSet

TEST_MEDIA_ROOT = settings.BASE_DIR / "test_media"


@override_settings(MEDIA_ROOT=TEST_MEDIA_ROOT)
def create_dataset():
    # NOTE: in a larger project, this it would be easier to generate
    # factories with factory-boy or similar.
    dataset = DataSet()

    with (pathlib.Path(__file__).parent / "test.csv").open("rb") as fp:
        dataset.upload.save("test.csv", ContentFile(fp.read()))

    dataset.save()
    return dataset


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
    def test_post_valid(self):
        with (pathlib.Path(__file__).parent / "test.csv").open("rb") as fp:
            response = self.client.post(
                self.url, {"upload": ContentFile("test.csv", fp.read)}
            )
        self.assertEqual(response.status_code, http.HTTPStatus.OK)
        self.assertTemplateUsed(response, "_upload.html")
