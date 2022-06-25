"""Contribs views."""
from typing import Any, Union

from django.http import HttpResponsePermanentRedirect, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse

from ..http import AuthenticatedHttpRequest
from ..models import User
from .mixins import TemplateAnonymousView, TemplateView
from .types import ContribsViewContextData


class ContribsView(TemplateAnonymousView):
    """Contribs view."""

    template_name = "contribs.html"

    def get_context_data(self, **kwargs: Any) -> ContribsViewContextData:  # type: ignore  # pylint: disable=no-self-use
        """Get context data."""
        user = get_object_or_404(User, username=kwargs["username"])
        repos = user.repos.all().prefetch_related("commits")
        return {"repos": repos, "selected_user": user}


class MyContribsView(TemplateView):
    """My contribs view."""

    template_name = ""

    def get(  # type: ignore
        self, request: AuthenticatedHttpRequest, *args: Any, **kwargs: Any  # pylint: disable=unused-argument
    ) -> Union[HttpResponseRedirect, HttpResponsePermanentRedirect]:
        """Get."""
        return redirect(reverse("contribs", args=(request.user.username,)))
