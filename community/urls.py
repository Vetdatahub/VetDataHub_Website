from django.urls import path

from analytics import views

urlpatterns = [
    path('',views.community,name='community')
]
