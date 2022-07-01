from http import HTTPStatus

from django.urls import reverse

from ..base import BaseTestLoginCase


class ContributionsTestCase(BaseTestLoginCase):
    """
    Tests for contributions.

    Dumpdata commands:
    manage dumpdata githubcontrib.Repo --indent 2 > githubcontrib/fixtures/repos.json
    manage dumpdata githubcontrib.Commit --indent 2 > githubcontrib/fixtures/commits.json

    User actions in fixtures:
    neo:
        - Added jieter/django-tables2
        - Added python-social-auth/social-core
        - Loaded commit data
    """

    fixtures = [
        "users.json",
        "repos.json",
    ]

    def contribs(self, page, with_username=True, status_code=HTTPStatus.OK):
        username = "neo"
        args = (username,) if with_username else None
        url = reverse(page, args=args)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status_code)
        if status_code == HTTPStatus.FOUND:
            response = self.client.get(url, follow=True)
        repos = list(response.context_data["repos"].values_list("pk", flat=True))
        self.assertListEqual(repos, [1, 2])
        self.assertEqual(response.context_data["selected_user"].username, username)

    def test_contribs(self):
        self.contribs("contribs")

    def test_contribs_anonymous(self):
        self.client.logout()
        self.contribs("contribs")

    def test_my_contribs(self):
        self.contribs("my_contribs", False, HTTPStatus.FOUND)

    def test_contribs_not_found(self):
        url = reverse("contribs", args=("potato",))
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
