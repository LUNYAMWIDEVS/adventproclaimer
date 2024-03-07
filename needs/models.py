from django.db import models

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=255)



class Need(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    category = models.ForeignKey(Category,on_delete=models.CASCADE,null=True,blank=True)
    price = models.DecimalField(decimal_places=4,max_digits=40)

class Requirements(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(decimal_places=4,max_digits=40)
    need = models.ForeignKey(Need,on_delete=models.CASCADE,null=True,blank=True)

