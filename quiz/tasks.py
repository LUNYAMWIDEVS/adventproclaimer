import requests
from celery.utils.log import get_task_logger
from django.conf import settings
from eLMS import celery_app
from celery import shared_task
from transformers import pipeline

logger = get_task_logger(__name__)



@shared_task
def start_pipeline(prompt):
    pipe = pipeline("text-generation", model="mistralai/Mixtral-8x7B-Instruct-v0.1")

    result = pipe(prompt, num_return_sequences=3)
    generated_answers = [item['generated_text'].split(':')[-1].strip() for item in result]

    print(generated_answers)