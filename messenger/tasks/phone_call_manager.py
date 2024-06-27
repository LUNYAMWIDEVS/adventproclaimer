import vonage
from celery import shared_task
import requests
import time
import os


VONAGE_APPLICATION_ID = os.getenv('VONAGE_APPLICATION_ID')
VONAGE_APPLICATION_PRIVATE_KEY_PATH = os.getenv('VONAGE_APPLICATION_PRIVATE_KEY_PATH')
VONAGE_NUMBER = os.getenv('VONAGE_NUMBER')

def split_text(text, max_length):
    """Split the text into blocks of max_length characters or fewer."""
    return [text[i:i+max_length] for i in range(0, len(text), max_length)]


@shared_task
def send_voice_over_call(to_number,text):
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
    
    text_blocks = split_text(text,max_length=500)
    stream_urls = []
    for text in text_blocks:
        url = "https://api.genny.lovo.ai/api/v1/tts/sync"
        
        
        payload = {
            "speed": 0.7,
            "speaker": chege['id'],
            "text": text
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
        stream_urls.append(stream_url)
    print(stream_urls)
    for stream_url in stream_urls:
        client = vonage.Client(
            application_id=VONAGE_APPLICATION_ID,
            private_key=VONAGE_APPLICATION_PRIVATE_KEY_PATH
        )

        # Create a new call and play the pre-recorded audio file
        response = client.voice.create_call({
            'to': [{'type': 'phone', 'number': to_number}],
            'from': {'type': 'phone', 'number': VONAGE_NUMBER},
            'ncco': [{'action': 'stream', 'streamUrl': [stream_url]}]
        })
        time.sleep(300)

        print(response)
