"""Types for views."""
from typing import TYPE_CHECKING

from django.db.models import QuerySet
from typing_extensions import TypedDict

if TYPE_CHECKING:
    from ..models import Repo, User  # pragma: no cover


class HomeViewContextData(TypedDict):
    """Home view context data."""

    usernames: list[str]


class ContribsViewContextData(TypedDict):
    """Contribs view context data."""

    repos: QuerySet["Repo"]
    selected_user: "User"


class MyReposViewContextData(TypedDict):
    """My repos view context data."""

    repos: str
