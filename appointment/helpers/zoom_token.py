import jwt
import datetime
import os 

def get_zoom_token(lasting_time):
    api_key = os.getenv('ZOOM_CLIENT_ID')
    api_secret = os.getenv('ZOOM_CLIENT_SECRET')

    payload = {
        'iss': api_key,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1)  # Token expiration time
    }

    token = jwt.encode(payload, api_secret, algorithm='HS256')
    return token