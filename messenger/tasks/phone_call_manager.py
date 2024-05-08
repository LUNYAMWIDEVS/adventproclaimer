import vonage
from celery import shared_task
import os


VONAGE_APPLICATION_ID = os.getenv('VONAGE_APPLICATION_ID')
VONAGE_APPLICATION_PRIVATE_KEY_PATH = os.getenv('VONAGE_APPLICATION_PRIVATE_KEY_PATH')
VONAGE_NUMBER = os.getenv('VONAGE_NUMBER')



@shared_task
def make_phone_call(to_number,message):
    client = vonage.Client(
            application_id=VONAGE_APPLICATION_ID,
            private_key=VONAGE_APPLICATION_PRIVATE_KEY_PATH,
        )
        
    response = client.voice.create_call({
        'to': [{'type': 'phone', 'number': to_number}],
        'from': {'type': 'phone', 'number': VONAGE_NUMBER},
        'ncco': [{'action': 'talk', 'text': message
                }]
    })