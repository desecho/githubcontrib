"""Contribs views."""

from http import HTTPStatus

from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from ..models import Commit, Repo, User


def serialize_commit(commit: Commit) -> dict[str, int | str]:
    """Serialize a commit."""
    return {
        "id": commit.pk,
        "url": commit.url,
        "date": commit.date.isoformat(),
        "message": commit.message,
    }


def serialize_repo(repo: Repo) -> dict[str, int | str | list[dict[str, int | str]]]:
    """Serialize a repo with commits."""
    return {
        "id": repo.pk,
        "name": repo.name,
        "commits": [serialize_commit(commit) for commit in repo.commits.all()],
    }


def serialize_contributions(
    user: User,
) -> dict[str, int | str | None | list[dict[str, int | str | list[dict[str, int | str]]]]]:
    """Serialize contribution page data."""
    repos = user.repos.all().prefetch_related("commits")
    return {
        "username": user.username,
        "avatar": user.avatar,
        "githubProfileUrl": user.github_profile_url,
        "stars": user.stars,
        "repos": [serialize_repo(repo) for repo in repos],
    }


class ContributionsView(APIView):
    """Contribs view."""

    permission_classes = [AllowAny]

    def get(self, request: Request, username: str) -> Response:
        """Get contributions for a user."""
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response(status=HTTPStatus.NOT_FOUND)

        return Response(serialize_contributions(user))


class MyContributionsView(APIView):
    """Current user contribs view."""

    def get(self, request: Request) -> Response:
        """Get current user's contribution route data."""
        user: User = request.user  # type: ignore[assignment]
        return Response(serialize_contributions(user))
