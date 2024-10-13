from django.contrib import admin
# Register your models here.
from .models import Dataset,Rating

admin.site.register(Dataset)
admin.site.register(Rating)