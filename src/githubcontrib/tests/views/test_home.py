from http import HTTPStatus

from django.urls import reverse

from ..base import BaseTestLoginCase


class HomeTestCase(BaseTestLoginCase):
    def test_users(self):
        url = reverse("users")
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertListEqual(response.json(), ["fox", "ironman"])

    def test_users_anonymous(self):
        self.client.force_authenticate(user=None)
        url = reverse("users")
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertListEqual(response.json(), ["fox", "ironman", "neo"])
