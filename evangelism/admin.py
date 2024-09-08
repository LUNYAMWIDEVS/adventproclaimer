from django.contrib import admin
from .models import BibleWorkerDailyReport,MedicalMissionaryDailyReport,AdventistMuslimRelationsDailyReport,Survey

# Register your models here.
admin.site.register(BibleWorkerDailyReport)
admin.site.register(MedicalMissionaryDailyReport)
admin.site.register(AdventistMuslimRelationsDailyReport)    
admin.site.register(Survey) 