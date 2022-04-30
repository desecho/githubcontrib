from typing import Any, Optional

from braces.views import JsonRequestResponseMixin, LoginRequiredMixin
from django.http import HttpResponse
from django.views.generic import TemplateView as TemplateViewOriginal, View


class AjaxAnonymousView(JsonRequestResponseMixin, View):
    MESSAGE_ERROR = "error"
    MESSAGE_INFO = "info"
    MESSAGE_WARNING = "warning"
    MESSAGE_SUCCESS = "success"

    def success(self, **kwargs: Any) -> HttpResponse:
        payload = {"status": "success"}
        payload.update(kwargs)
        response: HttpResponse = self.render_json_response(payload)
        return response

    def fail(self, message: Optional[str] = None, message_type: str = MESSAGE_ERROR) -> HttpResponse:
        payload = {"status": "fail", "message": message, "messageType": message_type}
        response: HttpResponse = self.render_json_response(payload)
        return response


class AjaxView(LoginRequiredMixin, AjaxAnonymousView):
    raise_exception = True


class TemplateView(LoginRequiredMixin, TemplateViewOriginal):
    pass


class TemplateAnonymousView(TemplateViewOriginal):
    pass
