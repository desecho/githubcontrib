import json

from bs4 import BeautifulSoup
from django.contrib.auth import get_user_model
from django.test import TestCase


class BaseTestCase(TestCase):
    # fixtures = [
    #     'users.json',
    # ]

    # USER_USERNAME = 'neo'
    # USER_PWD = 'password'
    # # Superuser - admin/adminpassword
    # # Another user - fox/password

    @staticmethod
    def get_content(response):
        return response.content.decode('utf-8')

    @staticmethod
    def get_soup(response):
        return BeautifulSoup(response.content)

    def get_json(self, response):
        return json.loads(self.get_content(response))

    def setUp(self):
        User = get_user_model()
        self.user = User.objects.get(username=self.USER_USERNAME)

    def login(self, username=None):
        if username is None:
            username = self.USER_USERNAME
        self.client.logout()
        self.client.login(
            username=username,
            password=self.USER_PWD
        )


class BaseTestLoginCase(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.login()
