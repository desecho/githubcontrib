# pylint: disable=redefined-outer-name

import github
import pytest
import requests
from flexmock import flexmock

from githubcontrib.github import Github

from .data.commit_items import commits1_items_data, commits2_items_page1_data, commits2_items_page2_data
from .fixtures import commits_python_social_auth as commits_python_social_auth_fixture, repo as repo_fixture


@pytest.fixture
def commits_python_social_auth():
    return commits_python_social_auth_fixture


@pytest.fixture
def commits1_items():
    return commits1_items_data


@pytest.fixture
def commits2_items_page1():
    return commits2_items_page1_data


@pytest.fixture
def commits2_items_page2():
    return commits2_items_page2_data


@pytest.fixture
def commits2_items_total(commits2_items_page1, commits2_items_page2):
    return commits2_items_page1 + commits2_items_page2


@pytest.fixture
def username():
    return "username"


@pytest.fixture
def repo():
    return repo_fixture


@pytest.fixture
def commits1_output(commits1_items):
    return {"total_count": 1, "incomplete_results": False, "items": commits1_items}


@pytest.fixture
def url_page1():
    return (
        "https://api.github.com/search/commits"
        "?q=author:desecho+repo:desecho/movies+sort:author-date-desc&per_page=100&page=1"
    )


@pytest.fixture
def url_page2():
    return (
        "https://api.github.com/search/commits"
        "?q=author:desecho+repo:desecho/movies+sort:author-date-desc&per_page=100&page=2"
    )


@pytest.fixture
def commits2_output_page1(commits2_items_page1):
    return {
        "total_count": 101,
        "incomplete_results": False,
        "items": commits2_items_page1,
    }


@pytest.fixture
def commits2_output_page2(commits2_items_page2):
    return {
        "total_count": 101,
        "incomplete_results": False,
        "items": commits2_items_page2,
    }


@pytest.fixture
def github_mock():
    return flexmock(spec=github.Github)


@pytest.fixture
def requests_mock():
    return flexmock(spec=requests)


@pytest.fixture
def githubcontrib_github_mock():
    return flexmock(spec=Github)


@pytest.fixture
def user_mock():
    return flexmock()


@pytest.fixture
def repo_mock():
    repo = flexmock()
    repo.owner = flexmock()
    repo.owner.login = "123"
    return repo


@pytest.fixture
def gh():
    return Github()
