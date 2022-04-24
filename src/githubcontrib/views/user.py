from django.conf import settings
from django.contrib.auth import logout
from django.shortcuts import redirect

from .mixins import AjaxView, TemplateView


def logout_view(request):
    logout(request)
    return redirect("/")


class PreferencesView(TemplateView):
    template_name = "user/preferences.html"


class SavePreferencesView(AjaxView):
    def post(self, request):
        def is_valid_language(language):
            for lang in settings.LANGUAGES:
                if lang[0] == language:
                    return True
            return False

        try:
            language = request.POST["language"]
        except KeyError:
            return self.render_bad_request_response()

        if not is_valid_language(language):
            return self.render_bad_request_response()

        user = request.user
        user.language = language
        user.save()
        return self.success()
