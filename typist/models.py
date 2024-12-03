from django.db import models

# Create your models here.

class Word(models.Model):
    text = models.CharField(max_length=100)

class UserScore(models.Model):
    user_name = models.CharField(max_length=100)
    score = models.IntegerField()