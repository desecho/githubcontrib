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
    def setUp(self):
        super().setUp()
        self.save_preferences_url = reverse("save_preferences")

    def test_preferences(self):
        url = reverse("preferences")
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_save_preferences(self):
        language = "ru"
        response = self.client.post_ajax(self.save_preferences_url, {"language": language})
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.json(), {"status": "success"})
        user = User.objects.get(pk=self.user.pk)
        self.assertEqual(user.language, language)

    def test_save_preferences_bad_request(self):
        response = self.client.post_ajax(self.save_preferences_url)
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)

    def test_save_preferences_invalid_language(self):
        response = self.client.post_ajax(self.save_preferences_url, {"language": "ro"})
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)


class AccountDeletedTestCase(BaseTestLoginCase):
    def test_account_deleted(self):
        url = reverse("account_deleted")
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)


class AccountDeleteTestCase(BaseTestLoginCase):
    def test_account_delete(self):
        url = reverse("delete_account")
        response = self.client.post(url)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertFalse(User.objects.filter(pk=self.user.pk).exists())
