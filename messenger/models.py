from django.db import models
from main.models import Student

# Create your models here.
class Message(models.Model):
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    sent = models.BooleanField(default=False)
    recipient = models.CharField(max_length=255)
    user = models.ForeignKey(Student,on_delete=models.CASCADE,null=True,blank=True)