from django.conf import settings
from django.utils.translation import activate


def language_middleware(get_response):
    def middleware(request):
        response = get_response(request)
        user = request.user
        if user.is_authenticated:
            language = user.language
            activate(language)
            response.set_cookie(settings.LANGUAGE_COOKIE_NAME, language)
        return response

    return middleware
