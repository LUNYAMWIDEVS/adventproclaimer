from django.contrib import admin
from .models import (Diagnosis, Disease, Cause, HydroTherapy, Symptom, Treatment)
# Register your models here.

admin.site.register(Diagnosis)
admin.site.register(Disease)
admin.site.register(Cause)
admin.site.register(HydroTherapy)
admin.site.register(Symptom)
admin.site.register(Treatment)