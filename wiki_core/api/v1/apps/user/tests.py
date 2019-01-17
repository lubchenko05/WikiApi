from rest_framework import status
from django.test import TestCase, Client
from django.urls import reverse


client = Client()


class GetUserToken(TestCase):
    fixtures = ['initial_data']

    def setUp(self):
        self.username = 'admin'
        self.password = 'admin'
        self.token = 'ee09cddebf71df4ebe5b6741197f081b4b0fb4ac'

    def test_get_token_with_valid_credentials(self):
        response = client.post(
            reverse('v1_token_auth'),
            data={'username': self.username, 'password': self.password},
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json().get('token'), self.token)

    def test_get_token_with_invalid_credentials(self):
        response = client.post(
            reverse('v1_token_auth'),
            data={'username': 'random', 'password': 'random'},
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json().get('non_field_errors', ['', ])[0], 'Unable to log in with provided credentials.')

