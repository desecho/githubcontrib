"""User views."""
from django.conf import settings
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import (
    HttpRequest,
    HttpResponse,
    HttpResponseBadRequest,
    HttpResponsePermanentRedirect,
    HttpResponseRedirect,
)
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic.edit import FormView

from ..forms import UserDeleteForm
from ..http import AuthenticatedHttpRequest
from ..types import UntypedObject
from .mixins import AjaxView, TemplateAnonymousView, TemplateView


def logout_view(request: HttpRequest) -> (HttpResponseRedirect | HttpResponsePermanentRedirect):
    """Return response for the logout view."""
    logout(request)
    return redirect("/")


class PreferencesView(TemplateView):
    """Preferences view."""

    template_name = "user/preferences.html"


class SavePreferencesView(AjaxView):
    """Save preferences view."""

    @staticmethod
    def _is_valid_language(language: str) -> bool:
        for lang in settings.LANGUAGES:
            if lang[0] == language:
                return True
        return False

    def post(self, request: AuthenticatedHttpRequest) -> (HttpResponse | HttpResponseBadRequest):
        """Return response for the save preferences view."""
        try:
            language = request.POST["language"]
        except KeyError:
            response_bad: HttpResponseBadRequest = self.render_bad_request_response()
            return response_bad

        if not self._is_valid_language(language):
            response: HttpResponse = self.render_bad_request_response()
            return response

        user = request.user
        user.language = language
        user.save()
        return self.success()


class AccountDeletedView(TemplateAnonymousView):
    """Account deleted view."""

    template_name = "user/account_deleted.html"


@method_decorator(login_required, name="dispatch")
class AccountDeleteView(FormView[UserDeleteForm]):  # pylint:disable=unsubscriptable-object
    """Account delete view."""

    template_name = "user/delete.html"
    form_class = UserDeleteForm

    def get_form_kwargs(self) -> UntypedObject:
        """Get form kwargs."""
        result = super().get_form_kwargs()
        result["instance"] = self.request.user
        return result

    def get_success_url(self) -> str:  # pylint:disable=no-self-use
        """Get success url."""
        return reverse("account_deleted")

    def form_valid(self, form: UserDeleteForm) -> HttpResponse:
        """Redirect to the supplied URL if the form is valid."""
        request = self.request
        request.user.delete()
        return super().form_valid(form)
