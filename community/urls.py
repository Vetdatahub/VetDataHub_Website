from django.urls import path
from community import views

urlpatterns = [
    path(
        "discussions/",
        views.discussion_list,
        name="discussion_list",
    ),
    path(
        "<int:dataset_id>/discussions/",
        views.discussion_list_by_dataset,
        name="discussion_list_by_dataset",
    ),
    path(
        "discussion/<slug:slug>/",
        views.discussion_detail,
        name="discussion_detail",
    ),
    path(
        "discussion/<int:dataset_id>/create-discussion/",
        views.create_discussion,
        name="create_discussion",
    ),
    path(
        "discussion/<slug:slug>/delete/",
        views.delete_discussion,
        name="delete_discussion",
    ),
    path(
        "comment/<int:comment_id>/edit/",
        views.edit_comment,
        name="edit_comment",
    ),
    path(
        "comment/<int:comment_id>/delete/",
        views.delete_comment,
        name="delete_comment",
    ),
]
