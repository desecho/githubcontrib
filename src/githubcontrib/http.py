from django.http import HttpRequest

from githubcontrib.models import User


class AuthenticatedHttpRequest(HttpRequest):
    user: User
