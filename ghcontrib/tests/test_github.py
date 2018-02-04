import github
import requests
from flexmock import flexmock
from github.GithubException import UnknownObjectException

from ghcontrib.github import Github

from .fixtures import (
    commits1_output,
    commits2_output_page1,
    commits2_output_page2,
    commits_python_social_auth,
    repo,
    url_page1,
    url_page2,
    username,
)
from .fixtures.commit_items import commits1_items, commits2_items_total

github_mock = flexmock(spec=github.Github)
ghcontrib_github_mock = flexmock(spec=Github)
user_mock = flexmock()
repo_mock = flexmock()
repo_mock.owner = flexmock()
repo_mock.owner.login = '123'

gh = Github()


def test_repo_exists_wrong_user():
    github_mock.should_receive('get_user').and_raise(UnknownObjectException(None, None))
    result = gh.repo_exists(repo)
    assert result is False


def test_repo_exists_wrong_repo():
    github_mock.should_receive('get_user').and_return(user_mock)
    user_mock.should_receive('get_repo').and_raise(UnknownObjectException(None, None))
    result = gh.repo_exists(repo)
    assert result is False


def test_repo_exists_user_mismatch():
    github_mock.should_receive('get_user').and_return(user_mock)
    user_mock.should_receive('get_repo').and_return(repo_mock)
    result = gh.repo_exists(repo)
    assert result is False


def test_repo_exists_success():
    github_mock.should_receive('get_user').and_return(user_mock)
    repo_mock.owner.login = username
    user_mock.should_receive('get_repo').and_return(repo_mock)
    result = gh.repo_exists(repo)
    assert result is True


def test_load_commits_one_page():
    ghcontrib_github_mock.should_receive('repo_exists').and_return(True)
    requests_mock = flexmock(spec=requests)
    response_mock = flexmock()
    response_mock.should_receive('json').and_return(commits1_output)
    requests_mock.should_receive('get').and_return(response_mock)
    result = gh._load_commits(username, repo, 1, [])  # pylint: disable=protected-access
    assert result == commits1_items


def test_load_commits_two_pages():
    ghcontrib_github_mock.should_receive('repo_exists').and_return(True)
    requests_mock = flexmock(spec=requests)
    response_mock_page1 = flexmock()
    response_mock_page1.should_receive('json').and_return(commits2_output_page1)
    requests_mock.should_receive('get').with_args(url_page1, headers=gh.HEADERS).and_return(response_mock_page1)
    response_mock_page2 = flexmock()
    response_mock_page2.should_receive('json').and_return(commits2_output_page2)
    requests_mock.should_receive('get').with_args(url_page2, headers=gh.HEADERS).and_return(response_mock_page2)

    result = gh._load_commits('desecho', 'desecho/movies', 1, [])  # pylint: disable=protected-access
    assert result == commits2_items_total


def test_get_commit_data_fail():
    ghcontrib_github_mock.should_receive('repo_exists').and_return(False)
    result = gh.get_commit_data(username, repo)
    assert result is None


def test_get_commit_data_success():
    ghcontrib_github_mock.should_receive('repo_exists').and_return(True)
    ghcontrib_github_mock.should_receive('_load_commits').and_return(commits1_items)
    result = gh.get_commit_data(username, repo)
    assert result == commits_python_social_auth
