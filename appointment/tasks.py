import os
import io
import time
import google.auth
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseUpload
from .helpers.zoom_token import get_zoom_token
import requests
import json
from celery import shared_task

# Set up the Zoom API client
zoom_api_url = "https://api.zoom.us/v2"
headers = {"authorization": f"Bearer {get_zoom_token(lasting_time=120)}", "content-type": "application/json"}

# Set up the OAuth 2.0 client for the Google API
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]
client_secret_file = os.path.join(os.path.dirname(__file__), "client_secret.json")


@shared_task
def upload_zoom_recording_to_youtube_task(meeting_id):
    # Wait until the Zoom meeting recording is ready for download
    recording_status = None
    
    response = requests.get(
        f"{zoom_api_url}/meetings/{meeting_id}/recordings",
        headers=headers,
        params={"recording_file_type": "mp4"},
    )
    response.raise_for_status()

    recording_files = response.json()["meetings"][0]["recording_files"]
    for recording in recording_files:
    # recording_file = next((f for f in recording_files if f["file_type"] == "MP4"), None)
        if recording_file["file_type"] == "MP4":
            if recording_file:
                recording_status = recording_file["status"]
            else:
                recording_status = None

            if recording_status != "completed":
                time.sleep(60)  # Wait for 60 seconds before checking again

            # Download the Zoom meeting recording from the Zoom API
            download_url = recording_file["download_url"]
            response = requests.get(download_url, stream=True)
            response.raise_for_status()
        
            # Upload the recording file to YouTube
            credentials = Credentials.from_authorized_user_file("client_secret.json", scopes)
            youtube = build("youtube", "v3", credentials=credentials)

            # Create the video metadata
            video_metadata = {
                "snippet": {
                    "categoryId": "22",  # Category for "People & Blogs"
                    "description": "Test Zoom meeting recording",
                    "title": "Test Zoom Meeting",
                },
                "status": {
                    "privacyStatus": "public",  # Set to "public" if you want the video to be public
                },
            }

            # Create the upload request
            request = youtube.videos().insert(
                part="snippet,status",
                body=video_metadata,
                media_body=MediaIoBaseUpload(io.BytesIO(response.content), mimetype="video/mp4", resumable=True),
            )
            response = request.execute()
            print(response)
        else:
            print("Not an mp4")
    

@shared_task
def create_zoom_meeting_task(topic, start_time, duration):
    # Create a new Zoom meeting
    data = {
        "topic": topic,
        "type": 2,  # Scheduled meeting
        "start_time": start_time,  # YYYY-MM-DDTHH:MM:SS
        "duration": duration,  # In minutes
        "timezone": "UTC",
    }
    response = requests.post(f"{zoom_api_url}/users/me/meetings", headers=headers, data=json.dumps(data))
    response.raise_for_status()

    # Return the meeting ID
    return response.json()["id"]
