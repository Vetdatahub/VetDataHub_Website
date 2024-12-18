from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from datasets.models import Dataset, DatasetVersion, Rating, Tag
from datasets.forms import (
    DatasetUploadForm,
    DatasetVersionForm,
    RatingForm,
)
from django.core.files.uploadedfile import SimpleUploadedFile


class DatasetTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create user
        cls.user = get_user_model().objects.create_user(
            username="testuser", password="testpassword"
        )

        # Create tags
        cls.tag = Tag.objects.create(name="Science")

        # Create a dataset
        cls.dataset = Dataset.objects.create(
            name="Test Dataset",
            description="Test description",
            dataset_type="image",
        )
        cls.dataset.tags.add(cls.tag)

        # Create a dataset version
        cls.version_file = SimpleUploadedFile(
            "test_version.csv", b"file_content"
        )
        cls.version = DatasetVersion.objects.create(
            dataset=cls.dataset,
            version_number=1,
            description="Initial version",
            file=cls.version_file,
            created_by=cls.user,
            is_latest=True,
        )

        # Create a rating
        cls.rating = Rating.objects.create(
            user=cls.user, dataset=cls.dataset, rating=4, review="Great dataset"
        )

        # Client for authentication
        cls.client = Client()


class ModelTests(DatasetTestCase):
    def test_dataset_model_str(self):
        self.assertEqual(str(self.dataset), "Test Dataset")

    def test_version_model_str(self):
        self.assertEqual(str(self.version), f"{self.dataset.name} (v1)")

    def test_average_rating(self):
        avg_rating = self.dataset.average_rating
        self.assertEqual(avg_rating, 4)

    def test_dataset_versions(self):
        self.assertEqual(len(self.dataset.get_all_versions), 1)

    def test_rating_model_str(self):
        self.assertEqual(
            str(self.rating),
            f"{self.user} rated {self.dataset} - 4 stars",
        )

    def test_tag_model_str(self):
        self.assertEqual(str(self.tag), "Science")


class FormTests(DatasetTestCase):
    def test_dataset_upload_form_valid(self):
        form_data = {
            "name": "Dataset 2",
            "description": "Another dataset",
            "tags": [self.tag.id],
            "dataset_type": "text",
            "version_description": "Initial version",
        }
        form_file = SimpleUploadedFile("file.csv", b"file_content")
        form = DatasetUploadForm(data=form_data, files={"file": form_file})
        self.assertTrue(form.is_valid())

    def test_dataset_version_form_valid(self):
        form_data = {"description": "New version"}
        form_file = SimpleUploadedFile("version2.csv", b"new_content")
        form = DatasetVersionForm(
            data=form_data,
            files={"file": form_file},
            user=self.user,
            dataset=self.dataset,
        )
        self.assertTrue(form.is_valid())


class ViewTests(DatasetTestCase):
    def setUp(self):
        self.client.login(username="testuser", password="testpassword")

    # Dataset Upload View
    def test_upload_dataset_view(self):
        upload_url = reverse("datasets:add_dataset")
        with open("upload_file.csv", "wb") as f:
            f.write(b"content")
        with open("upload_file.csv", "rb") as file:
            response = self.client.post(
                upload_url,
                {
                    "name": "New Dataset",
                    "description": "Uploaded dataset",
                    "tags": [self.tag.id],
                    "dataset_type": "audio",
                    "file": file,
                    "version_description": "Version 1",
                },
                follow=True,
            )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Dataset.objects.filter(name="New Dataset").exists())

    # Dataset List View
    def test_dataset_list_view(self):
        response = self.client.get(reverse("datasets:dataset_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.dataset.name)

    # Dataset Detail View
    def test_dataset_detail_view(self):
        response = self.client.get(
            reverse("datasets:dataset_detail", kwargs={"pk": self.dataset.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Initial version")
        self.assertContains(response, "4")

    # Add Dataset Version View
    def test_add_version_view(self):
        add_version_url = reverse(
            "datasets:add_dataset_version",
            kwargs={"dataset_id": self.dataset.pk},
        )
        form_file = SimpleUploadedFile("version2.csv", b"new_content")
        response = self.client.post(
            add_version_url,
            {"file": form_file, "description": "Version 2"},
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            DatasetVersion.objects.filter(version_number=2).exists()
        )

    # Rate Dataset View
    def test_rate_dataset_view(self):
        rate_url = reverse(
            "datasets:rate_dataset", kwargs={"dataset_id": self.dataset.pk}
        )
        response = self.client.post(
            rate_url,
            {"rating": 5, "review": "Excellent dataset"},
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            Rating.objects.filter(rating=5, review="Excellent dataset").exists()
        )
