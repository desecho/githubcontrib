from django.contrib.auth import logout
from django.shortcuts import redirect

from .mixins import TemplateView


def logout_view(request):
    logout(request)
    return redirect('/')


class PreferencesView(TemplateView):
    template_name = 'user/preferences.html'
