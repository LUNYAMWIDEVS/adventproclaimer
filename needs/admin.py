from django.contrib import admin
from .models import Need,Category, Requirements

# Register your models here.

admin.site.register(Need)
admin.site.register(Category)
admin.site.register(Requirements)