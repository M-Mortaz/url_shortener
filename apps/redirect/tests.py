from django.test import TestCase
from django.test import Client
from django.utils import timezone
from unittest.mock import patch
from datetime import timedelta
from apps.shortener.models import URL


class TestUrlShorter(TestCase):

    # @patch('apps.shortener.something')
    def setUp(self):
        self.url = "https://google.com"

    # TDD
    def test_redirect(self):
        """
        testing if redirect working correctly.
        """
        url = URL.objects.create(short_url="test",
                                 original_url="http://test.com/"
                                 )
        client = Client()
        response = client.get(
            path=f'/r1/{url.short_url}',
        )
        self.assertEqual(response.status_code, 301)

