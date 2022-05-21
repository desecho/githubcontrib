from typing import Any

from django_tqdm import BaseCommand

from githubcontrib.models import User


class Command(BaseCommand):
    help = "Update stars"

    def handle(self, *args: Any, **options: Any) -> None:  # pylint: disable=unused-argument
        users = User.objects.all()
        t = self.tqdm(total=users.count())
        for user in users:
            user.fetch_stars()
            t.set_description(str(user))
            t.update()
