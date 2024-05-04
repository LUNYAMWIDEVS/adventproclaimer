from django.db import models
from payment.models import Payment
# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=255)



class Need(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    category = models.ForeignKey(Category,on_delete=models.CASCADE,null=True,blank=True)
    price = models.DecimalField(decimal_places=4,max_digits=40)
    received_payments = models.ManyToManyField(Payment)

    @property
    def calculate_balance(self):
        received_amounts = []
        if self.received_payments.exists():
            for payment in self.received_payments.all():
                print(payment.amount)
                received_amounts.append(payment.amount)
            total_received = sum(received_amounts)
            print(total_received)
            print(self.price - total_received)
            balance = self.price - total_received
            return balance
        else:
            return self.price

class Requirements(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(decimal_places=4,max_digits=40)
    need = models.ForeignKey(Need,on_delete=models.CASCADE,null=True,blank=True)

