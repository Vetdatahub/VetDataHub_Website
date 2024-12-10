from django.urls import path,re_path
from django.contrib.auth.decorators import  login_required
from .views import CreateProfileView,UpdateProfileView,ProfileView

app_name = 'registration'

urlpatterns = [
    path('create_profile/', login_required(CreateProfileView.as_view()), name='create_profile'),
    path('update/<str:pk>/', UpdateProfileView.as_view(), name='profile_update'),
    path('', login_required(ProfileView.as_view()), name='profile_home'),
   ]


