"""User list views."""

from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from ..models import User


class UsersView(APIView):
    """Users view."""

    permission_classes = [AllowAny]

    def get(self, request: Request) -> Response:
        """Get public user list."""
        users = User.objects.exclude(username="admin")
        user = request.user
        if user.is_authenticated:
            users = users.exclude(pk=user.pk)
        usernames = list(users.values_list("username", flat=True))
        return Response(usernames)
