"""Base code for tests."""

from django.test import TestCase
from rest_framework.test import APIClient

from githubcontrib.models import User

CONTENT_TYPE = "application/json"


class BaseClient(APIClient):
    """Base client class."""

    def post_json(self, path, data=None, **extra):
        """Perform a JSON POST request."""
        return self.post(path, data, format="json", **extra)

    def put_json(self, path, data=None, **extra):
        """Perform a JSON PUT request."""
        return self.put(path, data, format="json", **extra)


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
        user = User.objects.get(username=username)
        self.client.force_authenticate(user=user)

    @property
    def is_authenticated(self):
        """Return True if user is authenticated."""
        return self.client.handler._force_user is not None  # type: ignore[attr-defined]


class BaseTestLoginCase(BaseTestCase):
    """Base test class (authenticated)."""

    def setUp(self):
        """Set up test environment."""
        super().setUp()
        self.login()
