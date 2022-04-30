import json
import re
from typing import Any, Dict, Union

from django.http import HttpRequest  # pylint: disable=duplicate-code
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponsePermanentRedirect, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from githubcontrib.github import Github
from githubcontrib.models import Commit, Repo, User

from .mixins import AjaxView, TemplateAnonymousView, TemplateView


class AboutView(TemplateAnonymousView):
    template_name = "about.html"


class HomeView(TemplateAnonymousView):
    template_name = "home.html"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        users = User.objects.exclude(username="admin")
        user = self.request.user
        if user.is_authenticated:
            users = users.exclude(pk=user.pk)
        return {"usernames": users.values_list("username", flat=True)}


class ContribsView(TemplateAnonymousView):
    template_name = "contribs.html"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:  # pylint: disable=no-self-use
        user = get_object_or_404(User, username=kwargs["username"])
        repos = user.repos.all().prefetch_related("commits")
        return {"repos": repos, "selected_user": user}


class MyContribsView(TemplateView):
    template_name = ""

    def get(
        self, *args: Any, **kwargs: Any
    ) -> Union[HttpResponseRedirect, HttpResponsePermanentRedirect]:  # pylint: disable=unused-argument
        user: User = self.request.user  # type: ignore
        return redirect(reverse("contribs", args=(user.username,)))


class MyReposView(TemplateView):
    template_name = "my_repos.html"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        repos = self.request.user.repos.all()  # type: ignore
        repos = [{"id": repo.id, "name": repo.name} for repo in repos]
        kwargs["repos"] = json.dumps(repos)
        return kwargs


class RepoView(AjaxView):
    def post(self, request: HttpRequest) -> (HttpResponse | HttpResponseBadRequest):
        try:
            name = request.POST["name"]
        except KeyError:
            response: HttpResponseBadRequest = self.render_bad_request_response()
            return response

        if re.match(r".+/.+", name) is None:
            return self.fail(_("Repository name is incorrect"))
        user: User = request.user  # type: ignore
        username, __ = name.split("/")
        if username == user.username:
            return self.fail(_("You cannot add your own repository"), self.MESSAGE_WARNING)
        if Github().repo_exists(name):
            if not user.repos.filter(name=name).exists():
                repo_id = Repo.objects.create(name=name, user=user).pk
                return self.success(id=repo_id)
            return self.fail(_("Repository already exists"), self.MESSAGE_WARNING)
        return self.fail(_("Repository not found"))


class RepoDeleteView(AjaxView):
    def delete(self, request: HttpRequest, repo_id: int) -> HttpResponse:
        repos = request.user.repos.filter(pk=repo_id)  # type: ignore
        if repos.exists():
            repos.delete()
        else:
            return self.fail(_("Repository not found"))
        return self.success()


class LoadCommitDataView(AjaxView):
    def post(self, request: HttpRequest) -> HttpResponse:
        user: User = request.user  # type: ignore
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
