"""Githubcontrib views."""
import json
import re
from typing import Any, Union

from django.http import HttpResponse, HttpResponseBadRequest, HttpResponsePermanentRedirect, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from ..github import Github
from ..http import AuthenticatedHttpRequest
from ..models import Commit, Repo, User
from .mixins import AjaxView, TemplateAnonymousView, TemplateView
from .types import ContribsViewContextData, HomeViewContextData, MyReposViewContextData


class AboutView(TemplateAnonymousView):
    """About view."""

    template_name = "about.html"


class HomeView(TemplateAnonymousView):
    """Home view."""

    template_name = "home.html"

    def get_context_data(self, **kwargs: Any) -> HomeViewContextData:  # type: ignore
        """Get context data."""
        users = User.objects.exclude(username="admin")
        user = self.request.user
        if user.is_authenticated:
            users = users.exclude(pk=user.pk)
        usernames = list(users.values_list("username", flat=True))
        return {"usernames": usernames}


class ContribsView(TemplateAnonymousView):
    """Contribs view."""

    template_name = "contribs.html"

    def get_context_data(self, **kwargs: Any) -> ContribsViewContextData:  # type: ignore  # pylint: disable=no-self-use
        """Get context data."""
        user = get_object_or_404(User, username=kwargs["username"])
        repos = user.repos.all().prefetch_related("commits")
        return {"repos": repos, "selected_user": user}


class MyContribsView(TemplateView):
    """My contribs view."""

    template_name = ""

    def get(  # type: ignore
        self, request: AuthenticatedHttpRequest, *args: Any, **kwargs: Any  # pylint: disable=unused-argument
    ) -> Union[HttpResponseRedirect, HttpResponsePermanentRedirect]:
        """Get."""
        return redirect(reverse("contribs", args=(request.user.username,)))


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
        """Post."""
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
        """Delete."""
        repos = request.user.repos.filter(pk=repo_id)
        if repos.exists():
            repos.delete()
        else:
            return self.fail(_("Repository not found"))
        return self.success()


class LoadCommitDataView(AjaxView):
    """Load commit data view."""

    def post(self, request: AuthenticatedHttpRequest) -> HttpResponse:
        """Post."""
        user = request.user
        repos = user.repos.all()
        gh = Github()
        for repo in repos:
            commit_data = gh.get_commit_data(user.username, repo.name)
            Commit.objects.filter(repo=repo).delete()
            for commit in commit_data:
                url: str = commit["url"]
                message: str = commit["message"]
                Commit.objects.create(
                    repo=repo,
                    url=url,
                    message=message,
                    date=commit["date"],
                )
        return self.success()
