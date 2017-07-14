from braces.views import JsonRequestResponseMixin, LoginRequiredMixin
from django.views.generic import TemplateView as TemplateViewOriginal
from django.views.generic import View


class AjaxAnonymousView(JsonRequestResponseMixin, View):
    def success(self):
        return self.render_json_response({'status': 'success'})


class AjaxView(LoginRequiredMixin, AjaxAnonymousView):
    raise_exception = True


class TemplateView(LoginRequiredMixin, TemplateViewOriginal):
    pass


class TemplateAnonymousView(TemplateViewOriginal):
    pass
