from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.db.models import Avg


class Tag(models.Model):
    name = models.CharField(max_length=120, unique=True)


class Dataset(models.Model):
    """Dataset Model"""

    DATASET_TYPES = [
        ("image", "Image"),
        ("clinical", "Clinical Record"),
        ("text", "Text Data"),
        ("audio", "Audio Data"),
        ("video", "Video Data"),
        ("other", "Other Data"),
    ]

    name = models.CharField(max_length=255)
    description = models.TextField()
    tags = models.ManyToManyField(Tag, related_name="datasets")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    dataset_type = models.CharField(max_length=50, choices=DATASET_TYPES)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("dataset_detail", kwargs={"pk": self.pk})

    @property
    def get_all_versions(self):
        return self.versions.all()

    @property
    def average_rating(self):
        return self.ratings.aggregate(average=Avg("rating"))["average"] or 0


class DatasetVersion(models.Model):
    dataset = models.ForeignKey(
        Dataset, related_name="versions", on_delete=models.CASCADE
    )
    version_number = models.PositiveIntegerField()
    description = models.TextField(
        blank=True, help_text="Changes in this version"
    )
    created_by = models.ForeignKey(
        get_user_model(), on_delete=models.SET_NULL, null=True, blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to="datasets/%Y/%m/%d/")
    is_latest = models.BooleanField(
        default=False
    )  # Indicates if this is the latest version

    class Meta:
        unique_together = ("dataset", "version_number")
        ordering = ["-created_at"]  # Latest versions first

    def __str__(self):
        return f"{self.dataset.title} (v{self.version_number})"

    def save(self, *args, **kwargs):
        # Automatically set the version number
        if not self.pk:  # When creating a new version
            latest_version = (
                DatasetVersion.objects.filter(dataset=self.dataset)
                .order_by("-version_number")
                .first()
            )
            if latest_version:
                self.version_number = latest_version.version_number + 1
                latest_version.update(is_latest=False)
            else:
                self.version_number = 1

        # Mark this version as the latest
        self.is_latest = True
        super().save(*args, **kwargs)


class Rating(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    dataset = models.ForeignKey(
        Dataset, on_delete=models.CASCADE, related_name="ratings"
    )
    rating = models.IntegerField(
        choices=[(i, i) for i in range(1, 11)]
    )  # 1 to 10 rating
    review = models.TextField(blank=True, null=True)  # Optional review
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (
            "user",
            "dataset",
        )  # Ensure one rating per user per dataset

    def __str__(self):
        return f"{self.user} rated {self.dataset} - {self.rating} stars"

    def get_absolute_url(self):
        return reverse("rating_detail", kwargs={"pk": self.pk})
