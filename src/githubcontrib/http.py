"""HTTP classes."""
from django.http import HttpRequest

from .models import User
from .types import UntypedObject


class AuthenticatedHttpRequest(HttpRequest):
    """Authenticated HTTP request."""

    LANGUAGE_CODE = ""

    user: User


class AuthenticatedAjaxHttpRequest(AuthenticatedHttpRequest):
    """Authenticated AJAX request."""

    PUT: UntypedObject = {}
