"""Update avatars."""
from typing import Any

from django_tqdm import BaseCommand

from githubcontrib.github import Github
from githubcontrib.models import User


class Command(BaseCommand):
    """Command."""

    help = "Update avatars"

    def handle(self, *args: Any, **options: Any) -> None:  # pylint: disable=unused-argument
        """Execute command."""
        gh = Github().gh
        users = User.objects.all()
        t = self.tqdm(total=users.count(), unit="user")
        for user in users:
            gh_user = gh.get_user(user.username)
            user.avatar = gh_user.avatar_url
            user.save()
            t.set_description(str(user))
            t.update()
