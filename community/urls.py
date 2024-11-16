from django.urls import path
from community import views

urlpatterns = [
    path('dataset/<int:dataset_id>/discussions/', views.discussion_list, name='discussion_list'),
    path('discussion/<slug:slug>/', views.discussion_detail, name='discussion_detail'),
    path('dataset/<int:dataset_id>/create-discussion/', views.create_discussion, name='create_discussion'),
    path('discussion/<slug:slug>/delete/', views.delete_discussion, name='delete_discussion'),
    path('comment/<int:comment_id>/edit/', views.edit_comment, name='edit_comment'),

]

