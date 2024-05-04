from django.urls import path
from . import views

urlpatterns = [
    path("create_meeting/", views.create_zoom_meeting, name="create_zoom_meeting"),
    path("upload_to_youtube/<str:meeting_id>/", views.upload_to_youtube, name="upload_to_youtube"),
    # Add more URLs here for other views
]
