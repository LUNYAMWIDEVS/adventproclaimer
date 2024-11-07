from django import forms
from .models import BibleWorkerDailyReport,MedicalMissionaryDailyReport

class BibleWorkerDailyReportForm(forms.ModelForm):
    class Meta:
        model = BibleWorkerDailyReport
        fields = '__all__'


class MedicalMissionaryDailyReportForm(forms.ModelForm):
    class Meta:
        model = MedicalMissionaryDailyReport
        fields = '__all__'
