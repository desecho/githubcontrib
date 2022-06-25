"""Home view."""
from typing import Any

from ..models import User
from .mixins import TemplateAnonymousView
from .types import HomeViewContextData


class HomeView(TemplateAnonymousView):
    """Home view."""

    template_name = "home.html"

    def get_context_data(self, **kwargs: Any) -> HomeViewContextData:  # type: ignore
        """Get context data."""
        users = User.objects.exclude(username="admin")
        user = self.request.user
        if user.is_authenticated:
            users = users.exclude(pk=user.pk)
        usernames = list(users.values_list("username", flat=True))
        return {"usernames": usernames}
