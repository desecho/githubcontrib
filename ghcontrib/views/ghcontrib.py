import json
import re

from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext_lazy as _

from ..github import Github
from ..models import Commit, Repo, User
from .mixins import AjaxView, TemplateAnonymousView, TemplateView


class HomeView(TemplateAnonymousView):
    template_name = 'home.html'

    def get_context_data(self):
        users = User.objects.exclude(username='admin')
        user = self.request.user
        if user.is_authenticated:
            users = users.exclude(pk=user.pk)
        return {'usernames': users.values_list('username', flat=True)}


class ContribsView(TemplateAnonymousView):
    template_name = 'contribs.html'

    def get_context_data(self, username):
        user = get_object_or_404(User, username=username)
        return {'repos': user.repos.all(), 'username': username}


class MyContribsView(TemplateView):
    template_name = 'contribs.html'

    def get_context_data(self):
        user = self.request.user
        return {'repos': user.repos.all(), 'username': user.username}


class MyReposView(TemplateView):
    template_name = 'my_repos.html'

    def get_context_data(self, **kwargs):
        repos = [{'id': repo.id, 'name': repo.name} for repo in self.request.user.repos.all()]
        kwargs['repos'] = json.dumps(repos)
        return kwargs


class AddRepoView(AjaxView):
    def post(self, *args, **kwargs):  # pylint: disable=unused-argument
        name = self.request.POST['name']
        if re.match('.+/.+', name) is not None:
            if Github().repo_exists(name):
                user = self.request.user
                if not user.repos.filter(name=name).exists():
                    repo_id = Repo.objects.create(name=name, user=user).pk
                    return self.success(id=repo_id)
                return self.fail(_('Repository already exists'))
            return self.fail(_('Repository not found'))
        return self.fail(_('Repository name is incorrect'))


class DeleteRepoView(AjaxView):
    def post(self, *args, **kwargs):  # pylint: disable=unused-argument
        id_ = self.request.POST['id']
        user = self.request.user
        if user.repos.filter(pk=id_).exists():
            Repo.objects.filter(pk=id_).delete()
        return self.success()


class LoadCommitDataView(AjaxView):
    def post(self, *args, **kwargs):  # pylint: disable=unused-argument
        user = self.request.user
        repos = user.repos.all()
        gh = Github()
        for repo in repos:
            commit_data = gh.get_commit_data(user.username, repo.name)
            if commit_data is None:
                name = repo.name
                return self.fail(_(f'Repository {name} not found'))
            Commit.objects.filter(repo=repo).delete()
            for commit in commit_data:
                Commit.objects.create(repo=repo, url=commit['url'], message=commit['message'], date=commit['date'])
        return self.success()
