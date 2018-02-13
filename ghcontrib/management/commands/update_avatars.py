from django_tqdm import BaseCommand

from ghcontrib.github import Github
from ghcontrib.models import User


class Command(BaseCommand):
    help = 'Updates avatars'

    def handle(self, *args, **options):  # pylint: disable=unused-argument
        gh = Github().gh
        users = User.objects.all()
        t = self.tqdm(total=users.count())
        for user in users:
            gh_user = gh.get_user(user.username)
            user.avatar = gh_user.avatar_url
            user.save()
            t.set_description(str(user))
            t.update()
