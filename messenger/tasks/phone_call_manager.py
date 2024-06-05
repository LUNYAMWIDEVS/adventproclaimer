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
    # Get the media folder path
    media_root = os.environ.get('DJANGO_SETTINGS_MODULE')
    media_folder = os.path.join(os.path.dirname(media_root), 'media')

    url = "https://api.voicer.io/api/v1/tts"

    headers = {
        'Authorization': 'Bearer YOUR_API_KEY',
        'Content-Type': 'application/json'
    }

    data = {
        "voice": "swahili-voice",
        "text": "Your Swahili Text"
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))
    file_name = f'{file_name_prefix}.mp3'
    # Save the audio file in the media folder
    with open(os.path.join(media_folder, file_name), 'wb') as f:
        f.write(response.content)



    client = vonage.Client(
        application_id=VONAGE_APPLICATION_ID,
        private_key=VONAGE_APPLICATION_PRIVATE_KEY_PATH
    )

    # Replace 'YOUR_GOOGLE_DRIVE_LINK' with the modified Google Drive link
    stream_url = f'https://adventproclaimer.com/media/{file_name}'
    # or
    # stream_url = os.path.join(media_folder, file_name)
    

    # Create a new call and play the pre-recorded audio file
    response = client.voice.create_call({
        'to': [{'type': 'phone', 'number': to_number}],
        'from': {'type': 'phone', 'number': VONAGE_NUMBER},
        'ncco': [{'action': 'stream', 'stream_url': [stream_url]}]
    })

    print(response)
