# Create your views here.
import requests
import os
from django.shortcuts import render
from django.http import JsonResponse
from .helpers.zoom_token import get_zoom_token

def create_zoom_meeting(request):
    # Zoom API endpoint for creating a meeting
    zoom_api_url = "https://api.zoom.us/v2/users/me/meetings"

    # Zoom API token (replace 'YOUR_ZOOM_API_TOKEN' with your actual token)
    zoom_api_token = get_zoom_token(lasting_time=120)

    # Request headers including the API token
    headers = {
        'Authorization': f'Bearer {zoom_api_token}',
        'Content-Type': 'application/json'
    }

    # Request body with meeting details
    meeting_data = {
        'topic': 'My Zoom Meeting',
        'type': 1,  # 1 for instant meeting, 2 for scheduled meeting
        'start_time': '2024-04-03T12:00:00',  # Adjust start time as needed
        'duration': 60,  # Meeting duration in minutes
    }

    # Make a POST request to create the meeting
    response = requests.post(zoom_api_url, json=meeting_data, headers=headers)

    # Check if the request was successful
    if response.status_code == 201:  # 201 indicates the meeting was created successfully
        # Extract the meeting data from the response
        # Return meeting details as JSON response
        return JsonResponse({"success":True})
    else:
        # If the request failed, return error message
        error_message = {"error": "Failed to create Zoom meeting"}
        return JsonResponse(error_message, status=response.status_code)
