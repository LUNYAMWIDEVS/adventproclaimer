# setup/celery.py

import os
from celery import Celery
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "eLMS.settings")

CELERY_TASKS = [
    'messenger.tasks.email_manager',
    'messenger.tasks.whatsapp_manager',
    'main.helpers',
    'appointment.tasks',
]

app = Celery("eLMS",include=CELERY_TASKS)
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)