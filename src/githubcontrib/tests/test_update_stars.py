from unittest.mock import patch

from githubcontrib.github import Github
from githubcontrib.management.commands.update_stars import Command
from githubcontrib.models import User

from .base import BaseTestCase


class UpdateStarsTestCase(BaseTestCase):
    @patch.object(Github, "get_stars_count")
    def test_update_stars(self, get_stars_count_mock):
        stars = 5
        get_stars_count_mock.return_value = stars

        Command().handle()

        users = User.objects.all()
        for user in users:
            self.assertEqual(user.stars, stars)
