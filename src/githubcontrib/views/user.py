from django.conf import settings
from django.contrib.auth import logout
from django.http import (
    HttpRequest,
    HttpResponse,
    HttpResponseBadRequest,
    HttpResponsePermanentRedirect,
    HttpResponseRedirect,
)
from django.shortcuts import redirect

from githubcontrib.http import AuthenticatedHttpRequest

from .mixins import AjaxView, TemplateView


def logout_view(request: HttpRequest) -> (HttpResponseRedirect | HttpResponsePermanentRedirect):
    logout(request)
    return redirect("/")


class PreferencesView(TemplateView):
    template_name = "user/preferences.html"


class SavePreferencesView(AjaxView):
    def post(self, request: AuthenticatedHttpRequest) -> (HttpResponse | HttpResponseBadRequest):
        def is_valid_language(language: str) -> bool:
            for lang in settings.LANGUAGES:
                if lang[0] == language:
                    return True
            return False

        try:
            language = request.POST["language"]
        except KeyError:
            response_bad: HttpResponseBadRequest = self.render_bad_request_response()
            return response_bad

        if not is_valid_language(language):
            response: HttpResponse = self.render_bad_request_response()
            return response

        user = request.user
        user.language = language
        user.save()
        return self.success()
