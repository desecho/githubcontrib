"""User views."""

from http import HTTPStatus
from typing import cast
from urllib.parse import urlencode

from django.conf import settings
from django.contrib.auth import logout
from django.http import HttpRequest, HttpResponseRedirect
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from ..models import User


def serialize_user(user: User) -> dict[str, int | str | None]:
    """Serialize current user data."""
    return {
        "id": user.pk,
        "username": user.username,
        "avatar": user.avatar,
        "githubProfileUrl": user.github_profile_url,
        "stars": user.stars,
    }


def auth_success_view(request: HttpRequest) -> HttpResponseRedirect:
    """Redirect authenticated GitHub OAuth users back to the frontend with JWT tokens."""
    if not request.user.is_authenticated:
        return HttpResponseRedirect(settings.LOGIN_URL)

    user = request.user
    refresh = RefreshToken.for_user(user)
    params = urlencode(
        {
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "username": user.username,
        }
    )
    frontend_url = settings.FRONTEND_URL.rstrip("/")
    logout(request)
    return HttpResponseRedirect(f"{frontend_url}/auth/callback#{params}")


class MeView(APIView):
    """Current user view."""

    def get(self, request: Request) -> Response:
        """Get current user."""
        user = cast(User, request.user)
        return Response(serialize_user(user))

    def delete(self, request: Request) -> Response:
        """Delete current user account."""
        user = cast(User, request.user)
        user.delete()
        return Response(status=HTTPStatus.NO_CONTENT)
