from django.db import models

# Create your models here.


class Payment(models.Model):
    '''Defines attributes of the payments model'''
    STATUS = [
        ('O', 'Ok'),
        ('P', 'Pending'),
        ('C', 'Cancelled')
    ]
    TYPE = [
        ('M', 'Mpesa'),
        ('C', 'Credit Card')
    ]
    phone_number = models.CharField(db_index=True, max_length=15,null=True,blank=True)
    amount = models.DecimalField(max_digits=20, decimal_places=2,null=True,blank=True)
    status = models.CharField(
        max_length=1,
        choices=STATUS,
        default='P',
        null=True,blank=True
    )
    payment_types = models.CharField(
        max_length=1,
        choices=TYPE,
        default='M',
        null=True,blank=True
    )
    # transaction_id = models.CharField(max_length=20, unique=True)
    business_short_code = models.CharField(
        max_length=20, blank=True, null=True)
    ref_number = models.CharField(max_length=50, blank=True, null=True)
    # A timestamp representing when this object was created.
    created_at = models.DateTimeField(auto_now_add=True)

    # A timestamp reprensenting when this object was last updated.
    updated_at = models.DateTimeField(auto_now=True)


    class Meta:
        '''Defines the ordering of the
         orders if retrieved'''
        ordering = ('created_at',)

    def __str__(self):
        return self.status
