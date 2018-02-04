import re

from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse

from ..github import Github
from ..models import Commit, Repo, User
from .mixins import AjaxView, TemplateAnonymousView, TemplateView

ERROR_REPOSITORY_NOT_FOUND = 'Repository not found'


class HomeView(TemplateAnonymousView):
    template_name = 'home.html'

    def get_context_data(self):
        return {'usernames': User.objects.exclude(username='admin').values_list('username', flat=True)}


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
        kwargs['repos'] = self.request.user.repos.all()
        return kwargs


class AddRepoView(MyReposView):
    def post(self, *args, **kwargs):  # pylint: disable=unused-argument
        def add_repo():
            name = self.request.POST['name']
            if re.match('.+/.+', name) is not None:
                if Github().repo_exists(name):
                    user = self.request.user
                    if not user.repos.filter(name=name).exists():
                        Repo.objects.create(name=name, user=user)
                    return True
            return False

        result = add_repo()
        if not result:
            kwargs['error'] = ERROR_REPOSITORY_NOT_FOUND
        return self.get(*args, **kwargs)


class DeleteRepoView(AjaxView):
    def post(self, *args, **kwargs):  # pylint: disable=unused-argument
        id_ = self.request.POST['id']
        user = self.request.user
        if user.repos.filter(pk=id_).exists():
            Repo.objects.filter(pk=id_).delete()
        return redirect(reverse('my_repos_edit'))


class LoadCommitDataView(MyReposView):
    def post(self, *args, **kwargs):  # pylint: disable=unused-argument
        user = self.request.user
        repos = user.repos.all()
        gh = Github()
        for repo in repos:
            commit_data = gh.get_commit_data(user.username, repo.name)
            if commit_data is None:
                kwargs['error'] = ERROR_REPOSITORY_NOT_FOUND
                kwargs['repo'] = repo.name
                break
            Commit.objects.filter(repo=repo).delete()
            for commit in commit_data:
                Commit.objects.create(repo=repo, url=commit['url'], message=commit['message'], date=commit['date'])
        return self.get(*args, **kwargs)
