"""URL Configuration."""
from django.conf import settings
from django.conf.urls import include
from django.contrib import admin
from django.contrib.auth.views import LoginView
from django.urls import path, re_path
from django.views.i18n import JavaScriptCatalog

from githubcontrib.views.githubcontrib import (
    AboutView,
    ContribsView,
    HomeView,
    LoadCommitDataView,
    MyContribsView,
    MyReposView,
    RepoView,
)
from githubcontrib.views.user import PreferencesView, SavePreferencesView, logout_view

admin.autodiscover()

urlpatterns = []

if settings.DEBUG:  # pragma: no cover
    import debug_toolbar

    urlpatterns += [
        path("__debug__/", include(debug_toolbar.urls)),
    ]

urlpatterns += [
    path("about/", AboutView.as_view(), name="about"),
    # User
    path("login/", LoginView.as_view(template_name="user/login.html"), name="login"),
    path("logout/", logout_view, name="logout"),
    # Preferences
    path("preferences/", PreferencesView.as_view(), name="preferences"),
    path("save-preferences/", SavePreferencesView.as_view(), name="save_preferences"),
    # Services
    path("admin/", admin.site.urls),
    path("", include("social_django.urls", namespace="social")),
    path(
        "jsi18n/",
        JavaScriptCatalog.as_view(packages=("githubcontrib",), domain="djangojs"),
        name="javascript-catalog",
    ),
    path("i18n/", include("django.conf.urls.i18n")),
    path("rosetta/", include("rosetta.urls")),
    path("djga/", include("google_analytics.urls")),
    # -------------------------------------------------------------------------------------------
    path("", HomeView.as_view(), name="home"),
    path("my-repositories/", MyReposView.as_view(), name="my_repos"),
    path("my-contributions/", MyContribsView.as_view(), name="my_contribs"),
    re_path(r"repository/(?P<id>\d+)/", RepoView.as_view(), name="repo"),
    path("repository/", RepoView.as_view(), name="repo"),
    path("load-commit-data/", LoadCommitDataView.as_view(), name="load_commit_data"),
    # This route has to be in the end
    path("<str:username>/", ContribsView.as_view(), name="contribs"),
]
