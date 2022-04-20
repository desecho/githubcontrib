from unittest.mock import Mock, patch

from github import Github

from githubcontrib.models import User
from githubcontrib.social import load_user_data

from .base import BaseTestCase


class UpdateAvatarsTestCase(BaseTestCase):
    def test_load_user_data_initial_data_loaded_already(self):
        self.user.loaded_initial_data = True

        load_user_data(None, self.user)

    @patch.object(Github, "get_user")
    def test_load_user_data(self, get_user_mock):
        new_avatar_url = "http://new-url"
        user_mock = Mock()
        user_mock.avatar_url = new_avatar_url
        get_user_mock.return_value = user_mock

        load_user_data(None, self.user)

        user = User.objects.get(pk=self.user.pk)
        self.assertEqual(user.avatar, new_avatar_url)
        self.assertTrue(user.loaded_initial_data)
