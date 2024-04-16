from django.test import TestCase, Client
from unittest.mock import patch
from django.http import JsonResponse

class ZoomMeetingCreationTestCase(TestCase):
    @patch('appointment.views.requests.post')
    def test_create_zoom_meeting_success(self, mock_post):
        mock_response = {
            'status_code': 201,
            'json.return_value': {
                'id': '123456789',
                'topic': 'My Zoom Meeting',
                # Add other meeting details here
            }
        }
        mock_post.return_value = type('Response', (), mock_response)

        # Make a request to the view
        client = Client()
        response = client.post('/appointment/create-zoom-meeting/', {})
        
        # Assert that the response is successful
        self.assertEqual(response.status_code, 200)

        # Assert that the response contains the meeting details
        expected_response_data = {
            'success':True,
            # Add other expected meeting details here
        }
        self.assertJSONEqual(response.content, expected_response_data)

    @patch('appointment.views.requests.post')
    def test_create_zoom_meeting_failure(self, mock_post):
        mock_response = {
            'status_code': 400,  # or any other error status code
        }
        mock_post.return_value = type('Response', (), mock_response)

        # Make a request to the view
        client = Client()
        response = client.post('/appointment/create-zoom-meeting/', {})

        # Assert that the response indicates failure
        self.assertEqual(response.status_code, 400)
