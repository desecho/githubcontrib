import json
import re

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

    def get_context_data(self):
        users = User.objects.exclude(username="admin")
        user = self.request.user
        if user.is_authenticated:
            users = users.exclude(pk=user.pk)
        return {"usernames": users.values_list("username", flat=True)}


class ContribsView(TemplateAnonymousView):
    template_name = "contribs.html"

    def get_context_data(self, username):  # pylint: disable=no-self-use
        user = get_object_or_404(User, username=username)
        return {"repos": user.repos.all().prefetch_related("commits"), "selected_user": user}


class MyContribsView(TemplateView):
    template_name = ""

    def get(self, *args, **kwargs):  # pylint: disable=unused-argument
        return redirect(reverse("contribs", args=(self.request.user.username,)))


class MyReposView(TemplateView):
    template_name = "my_repos.html"

    def get_context_data(self, **kwargs):
        repos = [{"id": repo.id, "name": repo.name} for repo in self.request.user.repos.all()]
        kwargs["repos"] = json.dumps(repos)
        return kwargs


class RepoView(AjaxView):
    def post(self, request):
        name = request.POST["name"]
        if re.match(r".+/.+", name) is None:
            return self.fail(_("Repository name is incorrect"))
        user = request.user
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
    def delete(self, request, repo_id):
        repos = request.user.repos.filter(pk=repo_id)
        if repos.exists():
            repos.delete()
        else:
            return self.fail(_("Repository not found"))
        return self.success()


class LoadCommitDataView(AjaxView):
    def post(self, request):
        user = request.user
        repos = user.repos.all()
        gh = Github()
        for repo in repos:
            commit_data = gh.get_commit_data(user.username, repo.name)
            Commit.objects.filter(repo=repo).delete()
            for commit in commit_data:
                Commit.objects.create(
                    repo=repo,
                    url=commit["url"],
                    message=commit["message"],
                    date=commit["date"],
                )
        return self.success()
