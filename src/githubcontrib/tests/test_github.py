from unittest.mock import patch

from github import Github
from github.GithubException import UnknownObjectException

from .fixtures import commits_python_social_auth, repo, username

# pylint: disable=no-name-in-module


@patch.object(Github, "get_user")
def test_repo_exists_wrong_repo(get_user_mock, user_mock, gh):
    get_user_mock.return_value = user_mock
    user_mock.get_repo.side_effect = UnknownObjectException(None, None, None)

    result = gh.repo_exists(repo)

    assert result is False


@patch.object(Github, "get_user")
def test_repo_exists_user_mismatch(get_user_mock, user_mock, repo_mock, gh):
    get_user_mock.return_value = user_mock
    user_mock.get_repo.return_value = repo_mock

    result = gh.repo_exists(repo)

    assert result is False


@patch.object(Github, "get_user")
def test_repo_exists_success(get_user_mock, user_mock, repo_mock, gh):
    get_user_mock.return_value = user_mock
    repo_mock.owner.login = username
    user_mock.get_repo.return_value = repo_mock

    result = gh.repo_exists(repo)

    assert result is True


@patch.object(Github, "search_commits")
def test_get_commit_data(search_commits_mock, gh, commits_paginated_list_mock):
    search_commits_mock.return_value = commits_paginated_list_mock

    result = gh.get_commit_data(username, repo)

    assert result == commits_python_social_auth


@patch.object(Github, "get_user")
def test_get_stars_count(get_user_mock, user_mock, gh, repos_paginated_list_mock):
    get_user_mock.return_value = user_mock
    user_mock.get_repos.return_value = repos_paginated_list_mock

    result = gh.get_stars_count(username)

    assert result == 5
