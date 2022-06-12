"""Base code for tests."""
from django.test import TestCase
from django.test.client import Client

from githubcontrib.models import User

CONTENT_TYPE = "application/json"


class BaseClient(Client):
    """Base client class."""

    def post_ajax(
        self,
        path,
        data=None,
        content_type=CONTENT_TYPE,
        follow=False,
        secure=False,
        **extra,
    ):
        """Perform an AJAX POST request."""
        return self.post(path, data, content_type, follow, secure, **extra)

    def put_ajax(
        self,
        path,
        data="",
        content_type=CONTENT_TYPE,
        follow=False,
        secure=False,
        **extra,
    ):
        """Perform an AJAX PUT request."""
        return self.put(path, data, content_type, follow, secure, **extra)


class BaseTestCase(TestCase):
    """Base test case."""

    maxDiff = None
    client_class = BaseClient
    fixtures = [
        "users.json",
    ]
    USER_USERNAME = "neo"
    USER_PASSWORD = "password"
    # Superuser - admin/adminpassword
    # Another user - fox/password

    def setUp(self):
        """Set up test environment."""
        self.user = User.objects.get(username=self.USER_USERNAME)

    def login(self, username=None):
        """Login."""
        if username is None:
            username = self.USER_USERNAME
        self.client.logout()
        self.client.login(username=username, password=self.USER_PASSWORD)

    @property
    def is_authenticated(self):
        """Return True if user is authenticated."""
        return "_auth_user_id" in self.client.session.keys()


class BaseTestLoginCase(BaseTestCase):
    """Base test class (authenticated)."""

    def setUp(self):
        """Set up test environment."""
        super().setUp()
        self.login()
