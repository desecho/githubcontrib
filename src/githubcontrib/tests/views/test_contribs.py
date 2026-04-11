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

    def contribs(self, status_code=HTTPStatus.OK):
        url = reverse("contributions", args=("neo",))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status_code)
        data = response.json()
        repos = data["repos"]
        self.assertListEqual([repo["id"] for repo in repos], [1, 2])
        self.assertEqual(data["username"], "neo")
        self.assertEqual(data["githubProfileUrl"], "https://github.com/neo")

    def test_contribs(self):
        self.contribs()

    def test_contribs_anonymous(self):
        self.client.force_authenticate(user=None)
        self.contribs()

    def test_my_contribs(self):
        url = reverse("my_contributions")
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        data = response.json()
        repos = data["repos"]
        self.assertListEqual([repo["id"] for repo in repos], [1, 2])
        self.assertEqual(data["username"], "neo")
        self.assertEqual(data["githubProfileUrl"], "https://github.com/neo")

    def test_contribs_not_found(self):
        url = reverse("contributions", args=("potato",))
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
