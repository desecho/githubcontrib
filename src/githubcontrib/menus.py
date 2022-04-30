from django.http import HttpRequest
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from menu import Menu, MenuItem


def is_authenticated(request: HttpRequest) -> bool:
    return request.user.is_authenticated


Menu.add_item("main", MenuItem(_("Users"), reverse("home")))
Menu.add_item(
    "main",
    MenuItem(_("My Contributions"), reverse("my_contribs"), check=is_authenticated),
)
Menu.add_item("main", MenuItem(_("My Repositories"), reverse("my_repos"), check=is_authenticated))
