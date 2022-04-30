from typing import Any

from social_core.backends.base import BaseAuth

from githubcontrib.models import User

from .github import Github


def load_user_data(backend: BaseAuth, user: User, **kwargs: Any) -> None:  # pylint: disable=unused-argument
    if user.loaded_initial_data:
        return None

    gh = Github().gh
    gh_user = gh.get_user(user.username)
    user.avatar = gh_user.avatar_url
    user.loaded_initial_data = True
    user.save()

    return None
