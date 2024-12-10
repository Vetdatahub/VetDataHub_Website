from django.urls import path
from . import views

app_name = "datasets"

urlpatterns = [
    # Dataset URLs
    path("", views.dataset_list, name="dataset_list"),
    path("<int:pk>/", views.dataset_detail, name="dataset_detail"),
    path("upload/", views.upload_dataset, name="add_dataset"),
    # DatasetVersion URLs
    path(
        "<int:dataset_id>/add-version/",
        views.add_dataset_version,
        name="add_dataset_version",
    ),
    # Rating URLs
    path(
        "<int:dataset_id>/rate/",
        views.rate_dataset,
        name="rate_dataset",
    ),
]
