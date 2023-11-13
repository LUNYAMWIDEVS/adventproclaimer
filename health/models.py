from django.db import models

# Create your models here.
class Disease(models.Model):
    name=models.CharField(max_length=255)

class Symptom(models.Model):
    name = models.CharField(max_length=255)
    disease = models.ForeignKey(Disease, on_delete=models.CASCADE, null=True, blank=True)

class Cause(models.Model):
    name = models.CharField(max_length=255)
    disease = models.ForeignKey(Disease, on_delete=models.CASCADE, null=True, blank=True)

class HydroTherapy(models.Model):
    name = models.CharField(max_length=255)
    disease = models.ForeignKey(Disease, on_delete=models.CASCADE, null=True, blank=True)

class Treatment(models.Model):
    name = models.CharField(max_length=255)
    disease = models.ForeignKey(Disease, on_delete=models.CASCADE, null=True, blank=True)


class Diagnosis(models.Model):
    name = models.CharField(max_length=255)
    disease = models.CharField(max_length=255)
    symptoms = models.TextField()
    causes = models.TextField()
    hydro = models.TextField()
    treatments = models.TextField()

    
    