from braces.views import JsonRequestResponseMixin, LoginRequiredMixin
from django.http import HttpResponse
from django.views.generic import TemplateView as TemplateViewOriginal, View


class AjaxAnonymousView(JsonRequestResponseMixin, View):
    MESSAGE_ERROR = "error"
    MESSAGE_INFO = "info"
    MESSAGE_WARNING = "warning"
    MESSAGE_SUCCESS = "success"

    def success(self, **kwargs) -> HttpResponse:
        response = {"status": "success"}
        response.update(kwargs)
        return self.render_json_response(response)

    def fail(self, message: str = None, message_type: str = MESSAGE_ERROR) -> HttpResponse:
        response = {"status": "fail", "message": message, "messageType": message_type}
        return self.render_json_response(response)


class AjaxView(LoginRequiredMixin, AjaxAnonymousView):
    raise_exception = True


class TemplateView(LoginRequiredMixin, TemplateViewOriginal):
    pass


class TemplateAnonymousView(TemplateViewOriginal):
    pass
