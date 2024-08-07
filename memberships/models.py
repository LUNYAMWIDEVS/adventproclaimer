from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from datetime import datetime
import paypalrestsdk

# Configure PayPal SDK
paypalrestsdk.configure({
    "mode": settings.PAYPAL_MODE,
    "client_id": settings.PAYPAL_CLIENT_ID,
    "client_secret": settings.PAYPAL_CLIENT_SECRET
})

MEMBERSHIP_CHOICES = (
    ('Enterprise', 'ent'),
    ('Professional', 'pro'),
    ('Free', 'free')
)

class Membership(models.Model):
    slug = models.SlugField()
    membership_type = models.CharField(
        choices=MEMBERSHIP_CHOICES,
        default='Free',
        max_length=30)
    price = models.IntegerField(default=15)
    paypal_plan_id = models.CharField(max_length=40)

    def __str__(self):
        return self.membership_type

class UserMembership(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    paypal_customer_id = models.CharField(max_length=40)
    membership = models.ForeignKey(
        Membership, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.user.username

def post_save_usermembership_create(sender, instance, created, *args, **kwargs):
    user_membership, created = UserMembership.objects.get_or_create(
        user=instance)

    if not user_membership.paypal_customer_id:
        # Create a new PayPal customer (you might need to handle customer creation differently with PayPal)
        free_membership = Membership.objects.get(membership_type='Free')
        user_membership.paypal_customer_id = instance.email
        user_membership.membership = free_membership
        user_membership.save()

post_save.connect(post_save_usermembership_create,
                  sender=settings.AUTH_USER_MODEL)

class Subscription(models.Model):
    user_membership = models.ForeignKey(
        UserMembership, on_delete=models.CASCADE)
    paypal_subscription_id = models.CharField(max_length=40)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.user_membership.user.username

    @property
    def get_created_date(self):
        # Retrieve subscription details from PayPal
        subscription = paypalrestsdk.BillingAgreement.find(self.paypal_subscription_id)
        return datetime.strptime(subscription.create_time, '%Y-%m-%dT%H:%M:%SZ')

    @property
    def get_next_billing_date(self):
        # Retrieve subscription details from PayPal
        subscription = paypalrestsdk.BillingAgreement.find(self.paypal_subscription_id)
        return datetime.strptime(subscription.agreement_details.next_billing_date, '%Y-%m-%dT%H:%M:%SZ')
