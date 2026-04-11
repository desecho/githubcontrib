from http import HTTPStatus

from django.urls import reverse

from ..base import BaseTestCase


class HealthTestCase(BaseTestCase):
    def test_health(self):
        url = reverse("health")
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.json(), {"status": "ok"})
