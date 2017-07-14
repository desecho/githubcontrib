from django.shortcuts import redirect
from django.core.urlresolvers import reverse

from .mixins import TemplateAnonymousView, TemplateView
from ..models import Repo

class HomeView(TemplateAnonymousView):
    template_name = 'home.html'


class ReposView(TemplateAnonymousView):
    template_name = 'repos.html'
    def get_context_data(self):
        return {'users': paginate(self.users, self.request.GET.get('page'),
                                  settings.PEOPLE_ON_PAGE)}

    def get(self, *args, **kwargs):
        self.users = self.request.user.get_users(sort=True)
        return super().get(*args, **kwargs)


class MyReposView(TemplateView):
    template_name = 'my_repos.html'
    def get_context_data(self):
        return {'users': paginate(self.users, self.request.GET.get('page'),
                                  settings.PEOPLE_ON_PAGE)}

    def get(self, *args, **kwargs):
        self.users = self.request.user.get_users(sort=True)
        return super().get(*args, **kwargs)


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


class DeleteRepoView(TemplateView):
    template_name = ''
    def post(self, *args, **kwargs):
        id = self.request.POST['id']
        user = self.request.user
        if user.repos.filter(pk=id).exists():
            Repo.objects.filter(pk=id).delete()
        return redirect(reverse('my_repos_edit'))
