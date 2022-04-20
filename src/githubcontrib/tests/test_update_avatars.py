from unittest.mock import Mock, patch

from github import Github

from githubcontrib.management.commands.update_avatars import Command
from githubcontrib.models import User

from .base import BaseTestCase


class UpdateAvatarsTestCase(BaseTestCase):
    @patch.object(Github, "get_user")
    def test_update_avatars(self, get_user_mock):
        new_avatar_url = "http://new-url"
        user_mock = Mock()
        user_mock.avatar_url = new_avatar_url
        get_user_mock.return_value = user_mock

        Command().handle()

        users = User.objects.all()
        for user in users:
            self.assertEqual(user.avatar, new_avatar_url)
