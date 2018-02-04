from django.urls import reverse

from .base import BaseTestLoginCase


class GithubContribTestCase(BaseTestLoginCase):
    def test_home(self):
        url = reverse('home')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertListEqual(list(response.context_data['usernames']), ['fox', 'ironman'])

