from django.contrib import admin
from django.contrib.auth.models import Permission
from . import models
# Register your models here.
admin.site.register(Permission)
admin.site.register(models.CountModel)
admin.site.register(models.Company)
admin.site.register(models.Inventory)
admin.site.register(models.Catalog)
admin.site.register(models.Account)
admin.site.register(models.Order)
admin.site.register(models.Item)
admin.site.register(models.Transaction)
admin.site.register(models.Order_Item)
