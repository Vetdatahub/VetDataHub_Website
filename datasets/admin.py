from django.contrib import admin

# Register your models here.
from .models import Dataset, Rating,DatasetVersion,Tag

admin.site.register(Dataset)
admin.site.register(Rating)
admin.site.register(DatasetVersion)
admin.site.register(Tag)
