from django.db.models import Q
from django.shortcuts import render
from datasets.models import Dataset
from community.models import Discussion, Comment


def search(request):
    query = request.GET.get("q", "").strip()
    dataset_results, discussion_results, comment_results = [], [], []
    if query:
        # Separate queries for each model
        dataset_results = Dataset.objects.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )
        discussion_results = Discussion.objects.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        )
        comment_results = Comment.objects.filter(Q(content__icontains=query))

    return render(
        request,
        "search/search_results.html",
        {
            "query": query,
            "dataset_results": dataset_results,
            "discussion_results": discussion_results,
            "comment_results": comment_results,
        },
    )
