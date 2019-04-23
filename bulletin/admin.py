from django.contrib import admin

# Register your models here.
from . import models

admin.site.register(models.Adopter)
admin.site.register(models.Find_pet)