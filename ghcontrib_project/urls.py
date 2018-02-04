"""URL Configuration."""
from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth.views import login
from django.views.i18n import JavaScriptCatalog

from ghcontrib.views.ghcontrib import (
    AddRepoView,
    ContribsView,
    DeleteRepoView,
    HomeView,
    LoadCommitDataView,
    MyContribsView,
    MyReposView,
)
from ghcontrib.views.user import PreferencesView, logout_view, SavePreferencesView

admin.autodiscover()

urlpatterns = [
    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^my-repositories/$', MyReposView.as_view(), name='my_repos'),
    url(r'^delete-repository/$', DeleteRepoView.as_view(), name='delete_repo'),
    url(r'^add-repository/$', AddRepoView.as_view(), name='add_repo'),
    url(r'^my-contributions/$', MyContribsView.as_view(), name='my_contribs'),
    url(r'^load-commit-data/$', LoadCommitDataView.as_view(), name='load_commit_data'),
    # User
    url(r'^login/$', login, {'template_name': 'user/login.html'}, name='login'),
    url(r'^logout/$', logout_view, name='logout'),
    # Preferences
    url(r'^preferences/$', PreferencesView.as_view(), name='preferences'),
    url(r'^save-preferences/$', SavePreferencesView.as_view(), name='save_preferences'),

    # -------------------------------------------------------------------------------------------
    # Internal
    url(r'^admin/', admin.site.urls),
    url('', include('social_django.urls', namespace='social')),
    url(r'^jsi18n/$',
        JavaScriptCatalog.as_view(packages=('ghcontrib', ), domain='djangojs'),
        name='javascript-catalog'),
    url(r'^i18n/', include('django.conf.urls.i18n')),
    url(r'^rosetta/', include('rosetta.urls')),
    # -------------------------------------------------------------------------------------------
    url(r'^(?P<username>[\w\d_-]+)/$', ContribsView.as_view(), name='contribs'),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]
