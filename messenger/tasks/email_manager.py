from time import sleep
from django.core.mail import send_mail
from django.conf import settings
from celery import shared_task


@shared_task
def send_newsletter(subject,email_address, message):
    """Sends an email when the feedback form has been submitted."""
    sleep(20)  # Simulate expensive operation(s) that freeze Django
    send_mail(
        subject,
        f"\t{message}\n\nThank you!",
        settings.DEFAULT_FROM_EMAIL,
        [email_address],
        fail_silently=False,
    )