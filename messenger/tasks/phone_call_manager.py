import vonage
from celery import shared_task
import requests
import json


VONAGE_APPLICATION_ID = os.getenv('VONAGE_APPLICATION_ID')
VONAGE_APPLICATION_PRIVATE_KEY_PATH = os.getenv('VONAGE_APPLICATION_PRIVATE_KEY_PATH')
VONAGE_NUMBER = os.getenv('VONAGE_NUMBER')
VONAGE_NUMBER = os.environ.get("VONAGE_NUMBER")



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


@shared_task
def send_voice_over_call(to_number,file_name_prefix):
    url = "https://api.genny.lovo.ai/api/v1/speakers?sort="
    
    headers = {
        "accept": "application/json",
        "X-API-KEY": os.getenv('LOVO_API_KEY')
    }
    
    response = requests.get(url, headers=headers)
    speakers = response.json()
    chege = None
    for speaker in speakers['data']:
        if speaker['displayName']=="Chege Odhiambo":
            chege = speaker
    url = "https://api.genny.lovo.ai/api/v1/tts/sync"
    
    payload = {
        "speed": 1,
        "speaker": chege['id'],
        "text": "habari yako ndugu niambie habari za Yesu"
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "X-API-KEY": os.getenv('LOVO_API_KEY')
    }
    
    response = requests.post(url, json=payload, headers=headers)
    
    audio_data = response.json()

    stream_url = None
    for audio in audio_data['data']:
        stream_url = ''.join(audio['urls'])

    client = vonage.Client(
        application_id=VONAGE_APPLICATION_ID,
        private_key=VONAGE_APPLICATION_PRIVATE_KEY_PATH
    )

    # Replace 'YOUR_GOOGLE_DRIVE_LINK' with the modified Google Drive link
    

    # Create a new call and play the pre-recorded audio file
    response = client.voice.create_call({
        'to': [{'type': 'phone', 'number': to_number}],
        'from': {'type': 'phone', 'number': VONAGE_NUMBER},
        'ncco': [{'action': 'stream', 'stream_url': [stream_url]}]
    })

    print(response)
