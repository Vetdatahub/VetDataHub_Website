from django.contrib import admin

# Register your models here.
from community.models import Discussion, Comment

admin.site.register(Discussion)
admin.site.register(Comment)