from django.shortcuts import render, redirect,get_object_or_404

from datasets.forms import DatasetUploadForm,DatasetVersionForm,RatingForm,TagForm
from datasets.models import  Dataset,DatasetVersion,Rating


@login_required
def upload_dataset(request):
    if request.method == "POST":
        form = DatasetUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save(user=request.user)  # Pass the logged-in user
            return redirect("dataset_list")
    else:
        form = DatasetUploadForm()
    return render(request, "datasets/upload_dataset.html", {"form": form})

def dataset_list(request):
    datasets = Dataset.objects.all()
    return render(request, "datasets/dataset_list.html", {"datasets": datasets})

def dataset_detail(request, pk):
    dataset = get_object_or_404(Dataset, pk=pk)
    average_rating = dataset.ratings.aggregate(average=Avg('rating'))['average'] or 0
    user_rating = None
    if request.user.is_authenticated:
        user_rating = dataset.ratings.filter(user=request.user).first()
    return render(
        request,
        "datasets/dataset_detail.html",
        {"dataset": dataset, "average_rating": average_rating, "user_rating": user_rating},
    )

@login_required
def add_dataset_version(request, dataset_id):
    dataset = get_object_or_404(Dataset, pk=dataset_id)
    if request.method == "POST":
        form = DatasetVersionForm(request.POST, request.FILES)
        if form.is_valid():
            form.save(user=request.user, dataset=dataset)
            return redirect("dataset_detail", pk=dataset_id)
    else:
        form = DatasetVersionForm()
    return render(request, "datasets/add_version.html", {"form": form, "dataset": dataset})


@login_required
def rate_dataset(request, dataset_id):
    dataset = get_object_or_404(Dataset, pk=dataset_id)
    rating = Rating.objects.filter(user=request.user, dataset=dataset).first()
    if request.method == "POST":
        form = RatingForm(request.POST, instance=rating)
        if form.is_valid():
            form.save(user=request.user, dataset=dataset)
            return redirect("dataset_detail", pk=dataset.pk)
    else:
        form = RatingForm(instance=rating)
    return render(
        request,
        "datasets/rate_dataset.html",
        {"form": form, "dataset": dataset, "existing_rating": dataset.average_rating()},
    )
