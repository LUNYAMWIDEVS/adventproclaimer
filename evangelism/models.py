from django.db import models

# Create your models here.

class BibleWorkerDailyReport(models.Model):
    name = models.CharField(max_length=1024,null=True,blank=True)
    content = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)
    email = models.EmailField(null=True,blank=True)
    homes_visited = models.IntegerField(null=True,blank=True)
    studies_given = models.IntegerField(null=True,blank=True)
    

    # Add more fields as needed


class MedicalMissionaryDailyReport(models.Model):
    name = models.CharField(max_length=1024)
    content = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)

class AdventistMuslimRelationsDailyReport(models.Model):
    name = models.CharField(max_length=1024)
    content = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)


class Survey(models.Model):
    TYPES = (
        ('Bible Worker', 'Bible Worker'),
        ('Medical Missionary', 'Medical Missionary'),
        ('Adentist Muslim Relations', 'Adentist Muslim Relations'),
    )   
    DAYS = (
        ('Sunday', 'Sunday'),
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
    )
    name = models.CharField(max_length=1024,null=True,blank=True)
    scheduled_day = models.CharField(choices=DAYS,default='Sunday',null=True,blank=True)
    scheduled_time = models.TimeField(null=True,blank=True)
    interest_type = models.CharField(max_length=100,choices=TYPES, default='Bible Worker',null=True,blank=True)
    bible_worker = models.ForeignKey(BibleWorkerDailyReport,on_delete=models.CASCADE,null=True,blank=True)
    medical_missionary = models.ForeignKey(MedicalMissionaryDailyReport,on_delete=models.CASCADE,null=True,blank=True)  
    adventist_muslim_relations = models.ForeignKey(AdventistMuslimRelationsDailyReport,on_delete=models.CASCADE,null=True,blank=True)   
    date_posted = models.DateTimeField(auto_now_add=True)
    phone_number = models.CharField(max_length=50,null=True,blank=True)


    def __str__(self) -> str:
        return f"{self.name} - {self.scheduled_day} - {self.scheduled_time}"
