from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse


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

    LICENSE = [
        ("mit", "MIT"),
    ]

    name = models.CharField(max_length=255)
    description = models.TextField()
    tags = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_public = models.BooleanField(default=True)
    dataset_type = models.CharField(max_length=50, choices=DATASET_TYPES)
    license = models.CharField(max_length=50, choices=LICENSE)
    format = models.CharField(max_length=255)
    file = models.FileField(upload_to="datasets/")
    version = models.IntegerField(default=1)
    uploader = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("dataset_detail", kwargs={"pk": self.pk})


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
