from django.db import models

# Create your models here.

class BibleWorkerDailyReport(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)
    # Add more fields as needed


class MedicalMissionaryDailyReport(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)