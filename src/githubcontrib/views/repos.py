"""Repos views."""
import json
import re
from typing import Any

from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _

from ..github import Github
from ..http import AuthenticatedHttpRequest
from ..models import Commit, Repo
from .mixins import AjaxView, TemplateView
from .types import MyReposViewContextData


class MyReposView(TemplateView):
    """My repos view."""

    template_name = "my_repos.html"

    def get_context_data(self, **kwargs: Any) -> MyReposViewContextData:  # type: ignore
        """Get context data."""
        request: AuthenticatedHttpRequest = self.request  # type: ignore
        repos = [{"id": repo.id, "name": repo.name} for repo in request.user.repos.all()]
        return {"repos": json.dumps(repos)}


class RepoView(AjaxView):
    """Repo view."""

    def post(self, request: AuthenticatedHttpRequest) -> (HttpResponse | HttpResponseBadRequest):
        """Add repo."""
        try:
            name = request.POST["name"]
        except KeyError:
            response: HttpResponseBadRequest = self.render_bad_request_response()
            return response

        if re.match(r".+/.+", name) is None:
            return self.fail(_("Repository name is incorrect"))
        user = request.user
        username, __ = name.split("/")
        if username == user.username:
            return self.fail(_("You cannot add your own repository"), self.MESSAGE_WARNING)
        if Github().is_repo_exists(name):
            if not user.repos.filter(name=name).exists():
                repo_id = Repo.objects.create(name=name, user=user).pk
                return self.success(id=repo_id)
            return self.fail(_("Repository already exists"), self.MESSAGE_WARNING)
        return self.fail(_("Repository not found"))


class RepoDeleteView(AjaxView):
    """Repo delete view."""

    def delete(self, request: AuthenticatedHttpRequest, repo_id: int) -> HttpResponse:
        """Delete repo."""
        repos = request.user.repos.filter(pk=repo_id)
        if repos.exists():
            repos.delete()
        else:
            return self.fail(_("Repository not found"))
        return self.success()


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
            message=message,
            date=commit["date"],
        )


class LoadCommitDataView(AjaxView):
    """Load commit data view."""

    def post(self, request: AuthenticatedHttpRequest) -> HttpResponse:
        """Load commit data for all repos."""
        repos = request.user.repos.all()
        for repo in repos:
            load_commit_data(repo)
        return self.success()


class RepoLoadCommitDataView(AjaxView):
    """Repo load commit data view."""

    def post(self, request: AuthenticatedHttpRequest, repo_id: int) -> HttpResponse:
        """Load commit data."""
        repo = get_object_or_404(Repo, user=request.user, pk=repo_id)
        load_commit_data(repo)
        return self.success()
