from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.core.paginator import Paginator
from django.http import HttpResponseForbidden
from .models import Discussion, Comment
from .forms import DiscussionForm, CommentForm


def discussion_list(request, dataset_id):
    """
    Displays a paginated list of discussions for a specific dataset.
    """
    discussions = Discussion.objects.filter(dataset_id=dataset_id).order_by(
        "-created_at"
    )
    paginator = Paginator(discussions, 10)  # Show 10 discussions per page
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request, "community/discussion_list.html", {"page_obj": page_obj}
    )


@login_required
def discussion_detail(request, slug):
    """
    Displays details of a discussion, including comments.
    """
    discussion = get_object_or_404(Discussion, slug=slug)
    comments = discussion.comments.order_by("-created_at")
    if request.method == "POST":
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.created_by = request.user
            comment.discussion = discussion
            comment.save()
            return redirect(
                reverse("discussion_detail", args=[discussion.slug])
            )
    else:
        comment_form = CommentForm()

    return render(
        request,
        "community/discussion_detail.html",
        {
            "discussion": discussion,
            "comments": comments,
            "comment_form": comment_form,
        },
    )


@login_required
def create_discussion(request, dataset_id):
    """
    Allows a user to create a new discussion for a specific dataset.
    """
    if request.method == "POST":
        form = DiscussionForm(request.POST)
        if form.is_valid():
            discussion = form.save(commit=False)
            discussion.created_by = request.user
            discussion.dataset_id = dataset_id
            discussion.save()
            return redirect(reverse("discussion_list", args=[dataset_id]))
    else:
        form = DiscussionForm()

    return render(request, "community/create_discussion.html", {"form": form})


@login_required
def delete_discussion(request, slug):
    """
    Allows the author of a discussion to delete it.
    """
    discussion = get_object_or_404(Discussion, slug=slug)
    if request.user != discussion.created_by:
        return HttpResponseForbidden(
            "You are not allowed to delete this discussion."
        )
    dataset_id = discussion.dataset_id
    discussion.delete()
    return redirect(reverse("discussion_list", args=[dataset_id]))


@login_required
def edit_comment(request, comment_id):
    """
    Allows a user to edit their comment if within the editable time limit.
    """
    comment = get_object_or_404(Comment, id=comment_id)

    if request.user != comment.created_by:
        return HttpResponseForbidden(
            "You are not allowed to edit this comment."
        )

    if not comment.is_editable():
        return HttpResponseForbidden(
            "The edit window for this comment has expired."
        )

    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect(
                reverse("discussion_detail", args=[comment.discussion.slug])
            )
    else:
        form = CommentForm(instance=comment)

    return render(
        request,
        "discussions/edit_comment.html",
        {"form": form, "comment": comment},
    )
