from django.test import TestCase
from django.test import Client
from django.utils import timezone
from unittest.mock import patch
from datetime import timedelta


class TestUrlShorter(TestCase):

    # @patch('apps.shortener.something')
    def setUp(self):
        self.url = "https://google.com"

    # TDD
    def test_url_shortener_creation(self):
        """
        TDD: try to create a shorter url with successful response.
        """
        client = Client()
        headers = {
            'content_type': 'application/json'
        }

        data = {
            'url': self.url
        }

        response = client.post(
            path='/api/v1/url_shortener/',
            data=data,
            **headers
        )
        self.assertEqual(response.status_code, 201)
