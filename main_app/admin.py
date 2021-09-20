from django.contrib import admin
#importing models
from .models import Skate, Maintenance, Photo

# Register your models here.
admin.site.register(Skate)
admin.site.register(Maintenance)
admin.site.register(Photo)
