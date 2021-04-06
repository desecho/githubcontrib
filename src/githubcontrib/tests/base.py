import json

from django.contrib.auth import get_user_model
from django.test import TestCase


class BaseTestCase(TestCase):
    fixtures = [
        "users.json",
    ]
    USER_USERNAME = "neo"
    USER_PASSWORD = "password"
    # Superuser - admin/adminpassword
    # Another user - fox/password

    @staticmethod
    def get_content(response):
        return response.content.decode("utf-8")

    def get_json(self, response):
        return json.loads(self.get_content(response))

    @staticmethod
    def get_user_model():
        return get_user_model()

    def setUp(self):
        User = self.get_user_model()
        self.user = User.objects.get(username=self.USER_USERNAME)

    def login(self, username=None):
        if username is None:
            username = self.USER_USERNAME
        self.client.logout()
        self.client.login(username=username, password=self.USER_PASSWORD)

    @property
    def is_authenticated(self):
        return "_auth_user_id" in self.client.session.keys()


class BaseTestLoginCase(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.login()
