import json
from http import HTTPStatus
from unittest.mock import patch

from django.urls import reverse

from githubcontrib.github import Github
from githubcontrib.models import Commit

from ..base import BaseTestLoginCase
from ..fixtures import commits_jieter, commits_python_social_auth, repo


class ContribHomeTestCase(BaseTestLoginCase):
    def test_home(self):
        url = reverse("home")
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertListEqual(list(response.context_data["usernames"]), ["fox", "ironman"])

    def test_home_anonymous(self):
        self.client.logout()
        url = reverse("home")
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertListEqual(list(response.context_data["usernames"]), ["fox", "ironman", "neo"])


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


class ReposTestCase(BaseTestLoginCase):
    fixtures = [
        "users.json",
        "repos.json",
    ]

    def test_my_repos(self):
        url = reverse("my_repos")
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        repos = json.loads(response.context_data["repos"])
        self.assertListEqual(
            repos,
            [
                {"id": 1, "name": "jieter/django-tables2"},
                {"id": 2, "name": "python-social-auth/social-core"},
            ],
        )


class RepoTestCase(BaseTestLoginCase):
    fixtures = [
        "users.json",
        "repos.json",
    ]

    def setUp(self):
        super().setUp()
        self.url = reverse("repo")

    def test_add_repo_wrong_name(self):
        response = self.client.post(self.url, {"name": "something"})
        self.assertEqual(response.status_code, HTTPStatus.OK)
        expected_response = {
            "status": "fail",
            "message": "Repository name is incorrect",
            "messageType": "error",
        }
        self.assertEqual(response.json(), expected_response)

    def test_add_repo_own(self):
        response = self.client.post(self.url, {"name": "neo/blah"})
        self.assertEqual(response.status_code, HTTPStatus.OK)
        expected_response = {
            "status": "fail",
            "message": "You cannot add your own repository",
            "messageType": "warning",
        }
        self.assertEqual(response.json(), expected_response)

    @patch.object(Github, "repo_exists")
    def test_add_repo_success(self, repo_exists_mock):
        repo_exists_mock.return_value = True
        response = self.client.post(self.url, {"name": repo})
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.json(), {"status": "success", "id": 3})

    @patch.object(Github, "repo_exists")
    def test_add_repo_repo_not_found(self, repo_exists_mock):
        repo_exists_mock.return_value = False
        response = self.client.post(self.url, {"name": repo})
        self.assertEqual(response.status_code, HTTPStatus.OK)
        expected_response = {
            "status": "fail",
            "message": "Repository not found",
            "messageType": "error",
        }
        self.assertEqual(response.json(), expected_response)

    @patch.object(Github, "repo_exists")
    def test_add_repo_exists(self, repo_exists_mock):
        repo_exists_mock.return_value = True
        response = self.client.post(self.url, {"name": "jieter/django-tables2"})
        self.assertEqual(response.status_code, HTTPStatus.OK)
        expected_response = {
            "status": "fail",
            "message": "Repository already exists",
            "messageType": "warning",
        }
        self.assertEqual(response.json(), expected_response)

    def test_delete_repo(self):
        url = reverse("repo", args=(1,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.json(), {"status": "success"})
        repos = list(self.user.repos.all().values_list("pk", flat=True))
        self.assertListEqual(repos, [2])

    def test_delete_repo_does_not_exist(self):
        url = reverse("repo", args=(5,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        expected_response = {
            "status": "fail",
            "message": "Repository not found",
            "messageType": "error",
        }
        self.assertEqual(response.json(), expected_response)

    def test_delete_repo_bad_request(self):
        url = reverse("repo")
        response = self.client.delete(url)
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)


class LoadCommitDataTestCase(BaseTestLoginCase):
    fixtures = [
        "users.json",
        "repos.json",
    ]

    def setUp(self):
        super().setUp()
        self.url = reverse("load_commit_data")

    @patch.object(Github, "get_commit_data")
    def test_load_commit_data_success(self, get_commit_data_mock):
        def get_commit_data(username: str, repo: str):  # pylint: disable=unused-argument,redefined-outer-name
            if repo == "jieter/django-tables2":
                return commits_jieter
            if repo == "python-social-auth/social-core":
                return commits_python_social_auth
            return None

        get_commit_data_mock.side_effect = get_commit_data
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        commits = Commit.objects.filter(repo__user=self.user)
        self.assertListEqual(list(commits.values_list("pk", flat=True)), [3, 2, 1])
        self.assertIn("python-social-auth/social-core", commits[0].url)
        self.assertIn("jieter/django-tables2", commits[2].url)
