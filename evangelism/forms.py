from django import forms
from .models import BibleWorkerDailyReport,MedicalMissionaryDailyReport

class BibleWorkerDailyReportForm(forms.ModelForm):
    class Meta:
        model = BibleWorkerDailyReport
        fields = ['title', 'content']


class MedicalMissionaryDailyReportForm(forms.ModelForm):
    class Meta:
        model = MedicalMissionaryDailyReport
        fields = ['title', 'content']