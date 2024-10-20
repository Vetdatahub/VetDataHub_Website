from django.urls import path

from analytics import views

urlpatterns = [
    path('',views.moderations,name='moderations')
]
