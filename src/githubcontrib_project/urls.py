"""URL Configuration."""
import debug_toolbar
from django.conf import settings
from django.conf.urls import include
from django.contrib import admin
from django.contrib.auth.views import LoginView
from django.urls import path
from django.views.i18n import JavaScriptCatalog

from githubcontrib.types import URL
from githubcontrib.views.about import AboutView
from githubcontrib.views.contribs import ContribsView, MyContribsView
from githubcontrib.views.home import HomeView
from githubcontrib.views.repos import (
    LoadCommitDataView,
    MyReposView,
    RepoDeleteView,
    RepoLoadCommitDataView,
    RepoView,
    SaveReposOrderView,
)
from githubcontrib.views.user import (
    AccountDeletedView,
    AccountDeleteView,
    PreferencesView,
    SavePreferencesView,
    logout_view,
)

admin.autodiscover()

URLList = list[URL]

urlpatterns: URLList = []

if settings.DEBUG:  # pragma: no cover
    urlpatterns += [
        path("__debug__/", include(debug_toolbar.urls)),
    ]

urlpatterns += [
    path("about/", AboutView.as_view(), name="about"),
    #
    # User
    path("login/", LoginView.as_view(template_name="user/login.html"), name="login"),
    path("logout/", logout_view, name="logout"),
    path("account/delete/", AccountDeleteView.as_view(), name="delete_account"),
    path("account/deleted/", AccountDeletedView.as_view(), name="account_deleted"),
    #
    # Preferences
    path("preferences/", PreferencesView.as_view(), name="preferences"),
    path("save-preferences/", SavePreferencesView.as_view(), name="save_preferences"),
    #
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
    # -------------------------------------------------------------------------------------------
    path("", HomeView.as_view(), name="home"),
    #
    # Repos
    path("my-repositories/", MyReposView.as_view(), name="my_repos"),
    path("repository/<int:repo_id>/load-commit-data/", RepoLoadCommitDataView.as_view(), name="repo_load_commit_data"),
    path("repository/<int:repo_id>/", RepoDeleteView.as_view(), name="repo"),
    path("repository/", RepoView.as_view(), name="repo"),
    path("load-commit-data/", LoadCommitDataView.as_view(), name="load_commit_data"),
    path("save-repos-order/", SaveReposOrderView.as_view(), name="save_repos_order"),
    #
    # Contribs
    path("my-contributions/", MyContribsView.as_view(), name="my_contribs"),
    # This route has to be in the end
    path("<str:username>/", ContribsView.as_view(), name="contribs"),
]
