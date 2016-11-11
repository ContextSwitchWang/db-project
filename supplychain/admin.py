from django.contrib import admin
from django.contrib.auth.models import Permission
from . import models
# Register your models here.
admin.site.register(Permission)
admin.site.register(models.CountModel)
