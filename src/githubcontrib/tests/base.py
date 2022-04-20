from django.test import TestCase

from githubcontrib.models import User


class BaseTestCase(TestCase):
    fixtures = [
        "users.json",
    ]
    USER_USERNAME = "neo"
    USER_PASSWORD = "password"
    # Superuser - admin/adminpassword
    # Another user - fox/password

    def setUp(self):
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
