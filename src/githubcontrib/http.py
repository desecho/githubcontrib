"""HTTP classes."""
from django.http import HttpRequest

from .models import User


class AuthenticatedHttpRequest(HttpRequest):
    """Authenticated HTTP request."""

    user: User
