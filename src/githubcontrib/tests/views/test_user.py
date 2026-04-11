from http import HTTPStatus

from django.conf import settings
from django.urls import reverse

from githubcontrib.models import User

from ..base import BaseTestLoginCase


class MeTestCase(BaseTestLoginCase):
    def test_me(self):
        url = reverse("me")
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        data = response.json()
        self.assertEqual(data["id"], self.user.pk)
        self.assertEqual(data["username"], self.user.username)
        self.assertEqual(data["githubProfileUrl"], "https://github.com/neo")

    def test_account_delete(self):
        url = reverse("me")
        response = self.client.delete(url)
        self.assertEqual(response.status_code, HTTPStatus.NO_CONTENT)
        self.assertFalse(User.objects.filter(pk=self.user.pk).exists())

    def test_me_anonymous(self):
        self.client.force_authenticate(user=None)
        url = reverse("me")
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED)


class AuthSuccessTestCase(BaseTestLoginCase):
    def test_auth_success_redirects_with_tokens(self):
        self.client.force_authenticate(user=None)
        self.client.force_login(self.user)
        url = reverse("auth_success")
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        location = response["Location"]
        self.assertTrue(location.startswith(f"{settings.FRONTEND_URL}/auth/callback#"))
        self.assertIn("access=", location)
        self.assertIn("refresh=", location)
        self.assertIn("username=neo", location)
