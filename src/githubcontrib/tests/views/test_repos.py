from http import HTTPStatus
from unittest.mock import patch

from django.urls import reverse

from githubcontrib.github import Github
from githubcontrib.models import Commit, Repo

from ..base import BaseTestLoginCase
from ..fixtures import commits_jieter, commits_python_social_auth, repo


class ReposTestCase(BaseTestLoginCase):
    fixtures = [
        "users.json",
        "repos.json",
    ]

    def test_my_repos(self):
        url = reverse("repos")
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertListEqual(
            response.json(),
            [
                {"id": 1, "name": "jieter/django-tables2", "order": 0},
                {"id": 2, "name": "python-social-auth/social-core", "order": 0},
            ],
        )

    def test_my_repos_anonymous(self):
        self.client.force_authenticate(user=None)
        url = reverse("repos")
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED)


class RepoTestCase(BaseTestLoginCase):
    fixtures = [
        "users.json",
        "repos.json",
    ]

    def setUp(self):
        super().setUp()
        self.url = reverse("repos")

    def test_add_repo_wrong_name(self):
        response = self.client.post_json(self.url, {"name": "something"})
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        expected_response = {
            "detail": "Repository name is incorrect",
            "messageType": "error",
        }
        self.assertEqual(response.json(), expected_response)

    def test_add_repo_own(self):
        response = self.client.post_json(self.url, {"name": "neo/blah"})
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        expected_response = {
            "detail": "You cannot add your own repository",
            "messageType": "warning",
        }
        self.assertEqual(response.json(), expected_response)

    @patch.object(Github, "is_repo_exists")
    def test_add_repo_success(self, is_repo_exists_mock):
        is_repo_exists_mock.return_value = True
        response = self.client.post_json(self.url, {"name": repo})
        self.assertEqual(response.status_code, HTTPStatus.CREATED)
        self.assertEqual(response.json(), {"id": 3, "name": repo, "order": 0})

    @patch.object(Github, "is_repo_exists")
    def test_add_repo_repo_not_found(self, is_repo_exists_mock):
        is_repo_exists_mock.return_value = False
        response = self.client.post_json(self.url, {"name": repo})
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        expected_response = {
            "detail": "Repository not found",
            "messageType": "error",
        }
        self.assertEqual(response.json(), expected_response)

    @patch.object(Github, "is_repo_exists")
    def test_add_is_repo_exists(self, is_repo_exists_mock):
        is_repo_exists_mock.return_value = True
        response = self.client.post_json(self.url, {"name": "jieter/django-tables2"})
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        expected_response = {
            "detail": "Repository already exists",
            "messageType": "warning",
        }
        self.assertEqual(response.json(), expected_response)

    def test_add_repo_bad_request(self):
        response = self.client.post_json(self.url)
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)


class RepoDeleteTestCase(BaseTestLoginCase):
    fixtures = [
        "users.json",
        "repos.json",
    ]

    def test_delete_repo(self):
        url = reverse("repo", args=(1,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, HTTPStatus.NO_CONTENT)
        repos = list(self.user.repos.all().values_list("pk", flat=True))
        self.assertListEqual(repos, [2])

    def test_delete_repo_does_not_exist(self):
        url = reverse("repo", args=(5,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        expected_response = {
            "detail": "Repository not found",
            "messageType": "error",
        }
        self.assertEqual(response.json(), expected_response)


class LoadCommitDataTestCase(BaseTestLoginCase):
    fixtures = [
        "users.json",
        "repos.json",
    ]

    @patch.object(Github, "get_commit_data")
    def test_load_commit_data_success(self, get_commit_data_mock):
        def get_commit_data(username: str, repo: str):  # pylint: disable=unused-argument,redefined-outer-name
            if repo == "jieter/django-tables2":
                return commits_jieter
            if repo == "python-social-auth/social-core":
                return commits_python_social_auth
            return None

        get_commit_data_mock.side_effect = get_commit_data
        url = reverse("load_commit_data")
        response = self.client.post_json(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        commits = Commit.objects.filter(repo__user=self.user)
        self.assertListEqual(list(commits.values_list("pk", flat=True)), [3, 2, 1])
        self.assertIn("python-social-auth/social-core", commits[0].url)
        self.assertIn("jieter/django-tables2", commits[2].url)


class RepoLoadCommitDataTestCase(BaseTestLoginCase):
    fixtures = [
        "users.json",
        "repos.json",
    ]

    @patch.object(Github, "get_commit_data")
    def test_load_commit_data_success(self, get_commit_data_mock):
        def get_commit_data(username: str, repo: str):  # pylint: disable=unused-argument,redefined-outer-name
            if repo == "jieter/django-tables2":
                return commits_jieter
            return None

        get_commit_data_mock.side_effect = get_commit_data
        url = reverse("repo_load_commit_data", args=(1,))
        response = self.client.post_json(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        commits = Commit.objects.filter(repo__user=self.user)
        self.assertListEqual(list(commits.values_list("pk", flat=True)), [1])
        self.assertIn("jieter/django-tables2", commits[0].url)

    def test_load_commit_data_404(self):
        url = reverse("repo_load_commit_data", args=(5,))
        response = self.client.post_json(url)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)


class SaveReposOrderTestCase(BaseTestLoginCase):
    fixtures = [
        "users.json",
        "repos.json",
    ]

    def setUp(self):
        super().setUp()
        self.url = reverse("save_repos_order")

    def test_repos_order(self):
        response = self.client.put_json(self.url, {"repos": [{"id": 1, "order": 2}, {"id": 2, "order": 1}]})
        self.assertEqual(response.status_code, HTTPStatus.OK)
        repo1 = Repo.objects.get(pk=1)
        self.assertEqual(repo1.order, 2)
        repo2 = Repo.objects.get(pk=2)
        self.assertEqual(repo2.order, 1)

    def test_repos_order_bad_request(self):
        response = self.client.put_json(self.url)
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
