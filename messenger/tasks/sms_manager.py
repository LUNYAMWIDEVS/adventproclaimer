from celery import shared_task
import requests
import os

@shared_task
def send_sms(phone_number, message):
    """Send SMS using your preferred SMS service (Twilio, Africa's Talking, etc.)"""
    try:
        # Example using Africa's Talking API
        url = "https://api.africastalking.com/version1/messaging"
        
        headers = {
            "apiKey": os.getenv('AFRICAS_TALKING_API_KEY'),
            "Content-Type": "application/x-www-form-urlencoded"
        }
        
        data = {
            "username": os.getenv('AFRICAS_TALKING_USERNAME'),
            "to": phone_number,
            "message": message
        }
        
        response = requests.post(url, headers=headers, data=data)
        
        if response.status_code == 200:
            print(f"SMS sent successfully to {phone_number}")
            return True
        else:
            print(f"SMS sending failed: {response.text}")
            return False
            
    except Exception as e:
        print(f"SMS sending error: {e}")
        return False