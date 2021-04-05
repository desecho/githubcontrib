from django.test import TestCase

from githubcontrib.models import Commit


class BaseTestCase(TestCase):
    fixtures = [
        'users.json',
        'repos.json',
        'commits.json',
    ]

    def test_commit_string(self):
        commit = str(Commit.objects.get(pk=1))
        self.assertEqual(
            commit,
            'jieter/django-tables2 - Regression fix - revert commit 05d8d1d260fe1cfe61a89ef0ae09c78513022f3c (#423)')
