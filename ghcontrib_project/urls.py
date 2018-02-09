"""URL Configuration."""
from django.conf import settings
from django.conf.urls import include
from django.contrib import admin
from django.contrib.auth.views import login
from django.urls import path
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
from ghcontrib.views.user import (
    PreferencesView,
    SavePreferencesView,
    logout_view,
)

admin.autodiscover()

urlpatterns = []

if settings.DEBUG:  # pragma: no cover
    import debug_toolbar

    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]

urlpatterns += [
    # User
    path('login/', login, {'template_name': 'user/login.html'}, name='login'),
    path('logout/', logout_view, name='logout'),

    # Preferences
    path('preferences/', PreferencesView.as_view(), name='preferences'),
    path('save-preferences/', SavePreferencesView.as_view(), name='save_preferences'),

    # Services
    path('admin/', admin.site.urls),
    path('', include('social_django.urls', namespace='social')),
    path('jsi18n/',
        JavaScriptCatalog.as_view(packages=('ghcontrib', ), domain='djangojs'),
        name='javascript-catalog'),
    path('i18n/', include('django.conf.urls.i18n')),
    path('rosetta/', include('rosetta.urls')),
    path('djga/', include('google_analytics.urls')),
    # -------------------------------------------------------------------------------------------
    path(r'', HomeView.as_view(), name='home'),
    path(r'my-repositories/', MyReposView.as_view(), name='my_repos'),
    path(r'my-contributions/', MyContribsView.as_view(), name='my_contribs'),
    path(r'delete-repository/', DeleteRepoView.as_view(), name='delete_repo'),
    path(r'add-repository/', AddRepoView.as_view(), name='add_repo'),
    path(r'load-commit-data/', LoadCommitDataView.as_view(), name='load_commit_data'),
    # This route has to be in the end
    path(r'<str:username>/', ContribsView.as_view(), name='contribs'),
]
