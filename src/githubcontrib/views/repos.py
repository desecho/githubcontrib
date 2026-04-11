"""Repos views."""

import re
from http import HTTPStatus
from typing import Any, cast

from django.shortcuts import get_object_or_404
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from ..github import Github
from ..models import Commit, Repo, User


def serialize_repo(repo: Repo) -> dict[str, int | str]:
    """Serialize repo list item."""
    return {
        "id": repo.pk,
        "name": repo.name,
        "order": repo.order,
    }


def error(detail: str, message_type: str = "error", status: HTTPStatus = HTTPStatus.BAD_REQUEST) -> Response:
    """Return an API error response."""
    return Response({"detail": detail, "messageType": message_type}, status=status)


def get_user(request: Request) -> User:
    """Return authenticated user from request."""
    return cast(User, request.user)


class ReposView(APIView):
    """My repos view."""

    def get(self, request: Request) -> Response:
        """Get current user's repos."""
        user = get_user(request)
        return Response([serialize_repo(repo) for repo in user.repos.all()])

    def post(self, request: Request) -> Response:
        """Add repo."""
        try:
            name = request.data["name"]
        except KeyError:
            return Response(status=HTTPStatus.BAD_REQUEST)

        if not isinstance(name, str) or re.fullmatch(r"[^/]+/[^/]+", name) is None:
            return error("Repository name is incorrect")
        user = get_user(request)
        username, __ = name.split("/")
        if username == user.username:
            return error("You cannot add your own repository", "warning")
        if Github().is_repo_exists(name):
            if not user.repos.filter(name=name).exists():
                repo = Repo.objects.create(name=name, user=user)
                return Response(serialize_repo(repo), status=HTTPStatus.CREATED)
            return error("Repository already exists", "warning")
        return error("Repository not found", status=HTTPStatus.NOT_FOUND)


class RepoDeleteView(APIView):
    """Repo delete view."""

    def delete(self, request: Request, repo_id: int) -> Response:
        """Delete repo."""
        user = get_user(request)
        repos = user.repos.filter(pk=repo_id)
        if repos.exists():
            repos.delete()
        else:
            return error("Repository not found", status=HTTPStatus.NOT_FOUND)
        return Response(status=HTTPStatus.NO_CONTENT)


def load_commit_data(repo: Repo) -> None:
    """Load commit data."""
    gh = Github()
    commit_data = gh.get_commit_data(repo.user.username, repo.name)
    for commit in commit_data:
        url: str = commit["url"]
        message: str = commit["message"]
        Commit.objects.update_or_create(
            repo=repo,
            url=url,
            defaults={
                "message": message,
                "date": commit["date"],
            },
        )


class LoadCommitDataView(APIView):
    """Load commit data view."""

    def post(self, request: Request) -> Response:
        """Load commit data for all repos."""
        user = get_user(request)
        repos = user.repos.all()
        for repo in repos:
            load_commit_data(repo)
        return Response()


class RepoLoadCommitDataView(APIView):
    """Repo load commit data view."""

    def post(self, request: Request, repo_id: int) -> Response:
        """Load commit data."""
        user = get_user(request)
        repo = get_object_or_404(Repo, user=user, pk=repo_id)
        load_commit_data(repo)
        return Response()


class SaveReposOrderView(APIView):
    """Save repos order view."""

    def put(self, request: Request) -> Response:
        """Save repos order."""
        try:
            repos = request.data["repos"]
        except KeyError:
            return Response(status=HTTPStatus.BAD_REQUEST)

        if not isinstance(repos, list):
            return Response(status=HTTPStatus.BAD_REQUEST)

        user = get_user(request)
        for repo in repos:
            if not isinstance(repo, dict):
                return Response(status=HTTPStatus.BAD_REQUEST)
            try:
                repo_id = int(cast(Any, repo)["id"])
                order = int(cast(Any, repo)["order"])
            except (KeyError, TypeError, ValueError):
                return Response(status=HTTPStatus.BAD_REQUEST)
            # If repo id is not found we silently ignore it
            Repo.objects.filter(pk=repo_id, user=user).update(order=order)
        return Response()
