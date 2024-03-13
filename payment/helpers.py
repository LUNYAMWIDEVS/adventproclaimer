import requests
import logging
from django.conf import settings
import json
from requests.auth import HTTPBasicAuth
from datetime import datetime
import base64

class MpesaC2bCredential:
    consumer_key = settings.MPESA_CONSUMER_KEY
    consumer_secret = settings.MPESA_CONSUMER_SECRET
    api_URL = settings.MPESA_API_URL

class MpesaAccessToken:
    conc_token = MpesaC2bCredential.consumer_key+":"+MpesaC2bCredential.consumer_secret
    headers = {
        'Authorization': f'Basic {base64.b64encode(conc_token.encode()).decode("utf-8")}'
    }
    try:
        r = requests.get(MpesaC2bCredential.api_URL,
                        headers=headers)
    except Exception as error:
        logging.warning(error)

    mpesa_access_token = json.loads(r.text.encode('utf-8'))
    validated_mpesa_access_token = mpesa_access_token['access_token']
    
class LipanaMpesaPpassword:
    lipa_time = datetime.now().strftime('%Y%m%d%H%M%S')
    Business_short_code = settings.MPESA_SHORT_CODE
    passkey = settings.MPESA_PASSKEY
    data_to_encode = Business_short_code + passkey + lipa_time
    online_password = base64.b64encode(data_to_encode.encode())
    decode_password = online_password.decode('utf-8')