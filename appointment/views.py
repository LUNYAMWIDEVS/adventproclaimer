# Create your views here.
import requests
import os
import io
from django.shortcuts import render
from django.http import JsonResponse
from .helpers.zoom_token import get_zoom_token
import os
import google.auth
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseUpload
import requests
import json
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .tasks import upload_zoom_recording_to_youtube_task, create_zoom_meeting_task

zoom_api_url = "https://api.zoom.us/v2"
headers = {"authorization": f"Bearer {get_zoom_token(lasting_time=120)}", "content-type": "application/json"}

# Set up the OAuth 2.0 client for the Google API
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]
client_secret_file = os.path.join(os.path.dirname(__file__), "client_secret.json")


# @login_required
def create_zoom_meeting(request):
    topic = "Test Meeting"
    start_time = "2023-03-01T12:00:00"  # YYYY-MM-DDTHH:MM:SS
    duration = 60  # In minutes
    task_result = create_zoom_meeting_task.delay(topic, start_time, duration)


    # Redirect the user to the dashboard
    return render(request, template_name="dashboard.html")


# @login_required
def upload_to_youtube(request, meeting_id):
    # Download the Zoom meeting recording from the Zoom API
    task_result = upload_zoom_recording_to_youtube_task.delay(meeting_id)


    # Redirect the user to the dashboard
    return render(request, template_name="dashboard.html")