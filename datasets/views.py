from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from datasets.forms import (
    DatasetUploadForm,
    DatasetVersionForm,
    RatingForm,
    TagForm,
)
from datasets.models import Dataset, DatasetVersion, Rating


@login_required()
def upload_dataset(request):
    if request.method == "POST":
        form = DatasetUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save(user=request.user)  # Pass the logged-in user
            return redirect("datasets:dataset_list")
    else:
        form = DatasetUploadForm()
    return render(request, "datasets/upload_dataset.html", {"form": form})


def dataset_list(request):
    datasets = Dataset.objects.all()
    return render(request, "datasets/dataset_list.html", {"datasets": datasets})


@login_required()
def dataset_detail(request, pk):
    dataset = get_object_or_404(Dataset, pk=pk)
    average_rating = dataset.average_rating
    versions = dataset.get_all_versions
    print(versions)

    return render(
        request,
        "datasets/dataset_detail.html",
        {
            "dataset": dataset,
            "average_rating": average_rating,
            "versions": versions,
        },
    )


@login_required()
def add_dataset_version(request, dataset_id):
    dataset = get_object_or_404(Dataset, pk=dataset_id)
    if request.method == "POST":
        print(request.FILES)
        form = DatasetVersionForm(
            request.POST, request.FILES, user=request.user, dataset=dataset
        )
        if form.is_valid():
            form.save()
            return redirect("datasets:dataset_detail", pk=dataset_id)
        print(form.errors)
    else:
        form = DatasetVersionForm(user=request.user, dataset=dataset)
    return render(
        request, "datasets/add_version.html", {"form": form, "dataset": dataset}
    )


@login_required
def rate_dataset(request, dataset_id):
    user = request.user
    dataset = get_object_or_404(Dataset, pk=dataset_id)

    if request.method == "POST":
        # Get the rating and optional review from POST data
        new_rating = request.POST.get("rating", 1)
        review = request.POST.get(
            "review", ""
        )  # Default to empty string if no review
        rating = Rating.objects.filter(dataset=dataset, user=user).first()

        if rating:
            rating.rating = new_rating
            rating.review = review
            rating.save()
        else:
            # If no rating exists, create a new one
            Rating.objects.create(
                dataset=dataset, user=user, rating=new_rating, review=review
            )

        return redirect("dataset_detail", pk=dataset.pk)

    return redirect("dataset_detail", pk=dataset.pk)
