# pylint: disable=redefined-outer-name

from unittest.mock import Mock

import pytest

from githubcontrib.github import Github

from .fixtures import commits_python_social_auth


@pytest.fixture
def user_mock():
    return Mock()


@pytest.fixture
def repo_mock():
    repo = Mock()
    repo.owner = Mock()
    repo.owner.login = "123"
    return repo


@pytest.fixture
def gh():
    g = Github()
    g.MAX_NUMBER_OF_ITEMS = 1
    return g


@pytest.fixture
def paginated_list_mock():
    def get_page(page):
        if page == 0:
            return [commit_mock1]
        if page == 1:
            return [commit_mock2]
        if page == 2:
            return []
        return None

    committer_mock1 = Mock()
    committer_mock1.date = commits_python_social_auth[0]["date"]
    git_commit_mock1 = Mock()
    git_commit_mock1.html_url = commits_python_social_auth[0]["url"]
    git_commit_mock1.committer = committer_mock1
    git_commit_mock1.message = commits_python_social_auth[0]["message"]
    commit_mock1 = Mock()
    commit_mock1.commit = git_commit_mock1

    committer_mock2 = Mock()
    committer_mock2.date = commits_python_social_auth[1]["date"]
    git_commit_mock2 = Mock()
    git_commit_mock2.html_url = commits_python_social_auth[1]["url"]
    git_commit_mock2.committer = committer_mock2
    git_commit_mock2.message = commits_python_social_auth[1]["message"]
    commit_mock2 = Mock()
    commit_mock2.commit = git_commit_mock2

    paginated_list = Mock()
    paginated_list.get_page.side_effect = get_page
    return paginated_list
