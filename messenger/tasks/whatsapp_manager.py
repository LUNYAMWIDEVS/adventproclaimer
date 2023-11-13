from requests import Session
import json
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
from time import sleep
from celery import shared_task
import os

BASE_URL = os.getenv('BASE_URL').strip()
API_VERSION = os.getenv('API_VERSION').strip()
SENDER = os.getenv('SENDER').strip()
ENDPOINT = os.getenv('ENDPOINT').strip()
API_TOKEN = os.getenv('API_TOKEN').strip()
URL = BASE_URL + API_VERSION + SENDER + ENDPOINT

@shared_task
def send_batch_whatsapp_text(numbers,names,message):
    for i,number in enumerate(numbers):
        
        headers = {
            "Authorization": f"Bearer {API_TOKEN}",
            "Content-Type": "application/json"
        }
        parameters = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "type": "template",
            "template": {
                "name": "present_truth_message",
                "language": {"code": "en_gb"},
                "components": [{
                        "type":"body",
                        "parameters":[
                            {
                                "type":"text",
                                "text": names[i],
                            },
                            {
                                "type":"text",
                                "text": message
                            }]
                        
                    }]
                
                }

        }
        session = Session()
        session.headers.update(headers)
        try:
            response = session.post(URL, json=parameters)
            data = json.loads(response.text)
            print(f"data: {data}")
        except (ConnectionError, Timeout, TooManyRedirects) as e:
            print(e)



def send_batch_whatsapp_text_non_async(numbers,names,message):
    for i,number in enumerate(numbers):
        
        headers = {
            "Authorization": f"Bearer {API_TOKEN}",
            "Content-Type": "application/json"
        }
        parameters = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "type": "template",
            "template": {
                "name": "present_truth_message",
                "language": {"code": "en_gb"},
                "components": [{
                        "type":"body",
                        "parameters":[
                            {
                                "type":"text",
                                "text": names[i],
                            },
                            {
                                "type":"text",
                                "text": message
                            }]
                        
                    }]
                
                }

        }
        session = Session()
        session.headers.update(headers)
        try:
            response = session.post(URL, json=parameters)
            data = json.loads(response.text)
            print(f"data: {data}")
        except (ConnectionError, Timeout, TooManyRedirects) as e:
            print(e)
