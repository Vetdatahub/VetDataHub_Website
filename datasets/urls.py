from django.urls import path
from . import views

urlpatterns = [
    # Dataset URLs
    path("", views.dataset_list, name="dataset_list"),
    path("dataset/<int:pk>/", views.dataset_detail, name="dataset_detail"),
    path("dataset/upload/", views.upload_dataset, name="add_dataset"),
    # DatasetVersion URLs
    path(
        "dataset/<int:dataset_id>/add-version/",
        views.add_dataset_version,
        name="add_dataset_version",
    ),
    # Rating URLs
    path(
        "dataset/<int:dataset_id>/rate/",
        views.rate_dataset,
        name="rate_dataset",
    ),
]
