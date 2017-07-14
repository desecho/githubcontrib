from django.shortcuts import redirect
from django.core.urlresolvers import reverse

from .mixins import TemplateAnonymousView, TemplateView, AjaxView
from ..models import Repo, Commit, User
from ..commit_data_loader import load_commit_data


class HomeView(TemplateAnonymousView):
    template_name = 'home.html'
    def get_context_data(self):
        return {'usernames': User.objects.exclude(username='admin').values_list('username', flat=True)}


class ReposView(TemplateAnonymousView):
    template_name = 'repos.html'
    def get_context_data(self, username):
        return {'repos': User.objects.get(username=username).repos.all(), 'username': username}


class MyReposView(TemplateView):
    template_name = ''
    def get(self, *args, **kwargs):
        return redirect(reverse('repos', args=(self.request.user.username,)))


class MyReposEditView(TemplateView):
    template_name = 'my_repos_edit.html'
    def get_context_data(self):
        return {'repos': self.request.user.repos.all()}


class AddRepoView(TemplateView):
    template_name = ''
    def post(self, *args, **kwargs):
        name = self.request.POST['name']
        user = self.request.user
        if not user.repos.filter(name=name).exists():
            Repo.objects.create(name=name, user=user)
        return redirect(reverse('my_repos_edit'))


class DeleteRepoView(AjaxView):
    def post(self, *args, **kwargs):
        id = self.request.POST['id']
        user = self.request.user
        if user.repos.filter(pk=id).exists():
            Repo.objects.filter(pk=id).delete()
        return redirect(reverse('my_repos_edit'))


class LoadCommitDataView(TemplateView):
    template_name = ''
    def post(self, *args, **kwargs):
        user = self.request.user
        repos = user.repos.all()
        for repo in repos:
            commit_data = load_commit_data(user.username, repo.name)
            Commit.objects.filter(repo=repo).delete()
            for commit in commit_data:
                Commit.objects.create(repo=repo, url=commit['url'], message=commit['message'], date=commit['date'])
        return redirect(reverse('my_repos_edit'))

