"""Update stars."""
from typing import Any

from django_tqdm import BaseCommand

from githubcontrib.models import User


class Command(BaseCommand):
    """Command."""

    help = "Update stars"

    def handle(self, *args: Any, **options: Any) -> None:  # pylint: disable=unused-argument
        """Execute command."""
        users = User.objects.all()
        t = self.tqdm(total=users.count(), unit="user")
        for user in users:
            user.stars = user.fetch_stars()
            user.save()
            t.set_description(str(user))
            t.update()
