from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.PreviousOrder)
admin.site.register(models.Orders)
admin.site.register(models.WishList)
