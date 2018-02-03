"""URL Configuration."""
from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth.views import login

from ghcontrib.views.ghcontrib import (
    AddRepoView, DeleteRepoView, HomeView, LoadCommitDataView, MyReposEditView,
    MyReposView, ReposView,
)
from ghcontrib.views.user import PreferencesView, logout_view

admin.autodiscover()

urlpatterns = [
    url(r'^$', HomeView.as_view(), name='home'),

    # User
    url(r'^login/$', login, {'template_name': 'user/login.html'}, name='login'),
    url(r'^logout/$', logout_view, name='logout'),
    # Preferences
    url(r'^preferences/$', PreferencesView.as_view(), name='preferences'),

    url(r'^admin/', admin.site.urls),

    url('', include('social_django.urls', namespace='social')),
    url(r'^my-repos/edit/$', MyReposEditView.as_view(), name='my_repos_edit'),
    url(r'^delete-repo/$', DeleteRepoView.as_view(), name='delete_repo'),
    url(r'^add-repo/$', AddRepoView.as_view(), name='add_repo'),
    url(r'^my-repos/$', MyReposView.as_view(), name='my_repos'),
    url(r'^load-commit-data/$', LoadCommitDataView.as_view(), name='load_commit_data'),
    url(r'^(?P<username>[\w\d_-]+)/$', ReposView.as_view(), name='repos'),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]
