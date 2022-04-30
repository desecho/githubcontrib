from typing import Any, Dict

from django.conf import settings
from django.http import HttpRequest


def variables(request: HttpRequest) -> Dict[str, Any]:  # pylint: disable=unused-argument
    return {
        "DEBUG": settings.DEBUG,
        "ADMIN_EMAIL": settings.ADMIN_EMAIL,
        "GOOGLE_ANALYTICS_ID": settings.GOOGLE_ANALYTICS_ID,
    }
