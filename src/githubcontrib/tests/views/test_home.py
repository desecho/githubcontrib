from http import HTTPStatus

from django.urls import reverse

from ..base import BaseTestLoginCase


class HomeTestCase(BaseTestLoginCase):
    def test_home(self):
        url = reverse("home")
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertListEqual(list(response.context_data["usernames"]), ["fox", "ironman"])

    def test_home_anonymous(self):
        self.client.logout()
        url = reverse("home")
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertListEqual(list(response.context_data["usernames"]), ["fox", "ironman", "neo"])
