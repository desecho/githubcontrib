"""Social."""
from typing import Any

from social_core.backends.base import BaseAuth

from .github import Github
from .models import User


def load_user_data(backend: BaseAuth, user: User, **kwargs: Any) -> None:  # pylint: disable=unused-argument
    """Load user data."""
    if user.loaded_initial_data:
        return None

    gh = Github().gh
    gh_user = gh.get_user(user.username)
    user.avatar = gh_user.avatar_url
    user.loaded_initial_data = True
    user.fetch_stars(False)
    user.save()

    return None
