"""URL Configuration."""

from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from rest_framework_simplejwt.views import TokenRefreshView

from githubcontrib.types import URL
from githubcontrib.views.common import HealthView
from githubcontrib.views.contribs import ContributionsView, MyContributionsView
from githubcontrib.views.home import UsersView
from githubcontrib.views.repos import (
    LoadCommitDataView,
    RepoDeleteView,
    RepoLoadCommitDataView,
    ReposView,
    SaveReposOrderView,
)
from githubcontrib.views.user import MeView, auth_success_view

admin.autodiscover()

URLList = list[URL]

urlpatterns: URLList = []

if settings.DEBUG:  # pragma: no cover
    import debug_toolbar

    urlpatterns += [
        path("__debug__/", include(debug_toolbar.urls)),
    ]

urlpatterns += [
    # Health
    path("health/", HealthView.as_view(), name="health"),
    # Services
    path("admin/", admin.site.urls),
    # Auth
    path("auth/", include("social_django.urls", namespace="social")),
    path("auth/success/", auth_success_view, name="auth_success"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    # User
    path("me/", MeView.as_view(), name="me"),
    path("users/", UsersView.as_view(), name="users"),
    path("users/<str:username>/contributions/", ContributionsView.as_view(), name="contributions"),
    path("my-contributions/", MyContributionsView.as_view(), name="my_contributions"),
    # Repos
    path("repos/", ReposView.as_view(), name="repos"),
    path("repos/<int:repo_id>/", RepoDeleteView.as_view(), name="repo"),
    path("repos/load-commit-data/", LoadCommitDataView.as_view(), name="load_commit_data"),
    path("repos/<int:repo_id>/load-commit-data/", RepoLoadCommitDataView.as_view(), name="repo_load_commit_data"),
    path("repos/save-order/", SaveReposOrderView.as_view(), name="save_repos_order"),
]
