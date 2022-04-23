from http import HTTPStatus

from django.urls import reverse

from githubcontrib.models import User

from ..base import BaseTestLoginCase


class LogoutTestCase(BaseTestLoginCase):
    def test_logout(self):
        response = self.client.get(reverse("logout"))
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertFalse(self.is_authenticated)


class PreferencesTestCase(BaseTestLoginCase):
    def test_preferences(self):
        response = self.client.get(reverse("preferences"))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_save_preferences(self):
        language = "ru"
        response = self.client.post(reverse("save_preferences"), {"language": language})
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.json(), {"status": "success"})
        user = User.objects.get(pk=self.user.pk)
        self.assertEqual(user.language, language)

    def test_save_preferences_bad_request(self):
        response = self.client.post(reverse("save_preferences"))
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
