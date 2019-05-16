import datetime

import requests
from dateutil.tz import tzoffset
import pytest
import github
from flexmock import flexmock

from ghcontrib.github import Github

from .data.commit_items import commits1_items_data, commits2_items_page1_data, commits2_items_page2_data


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
def commits_jieter():
    return [{
        'url': 'https://github.com/jieter/django-tables2/commit/360b29c5948c1f9bada618c30897e380e21a4f0a',
        'date': datetime.datetime(2017, 3, 6, 13, 30, 58, tzinfo=tzoffset(None, 3600)),
        'message': 'Regression fix - revert commit 05d8d1d260fe1cfe61a89ef0ae09c78513022f3c (#423)'
    }]


@pytest.fixture
def commits_python_social_auth():
    return [{
        'url':
        'https://github.com/python-social-auth/social-core/commit/ab19dc49a5366ae4f917bed2a7bfddce7e7b003f',
        'date':
        datetime.datetime(2017, 4, 16, 4, 39, 32, tzinfo=tzoffset(None, -14400)),
        'message':
        'Speed up authorization process for VKAppOAuth2\nUse first api request provided immediately instead of creating a new one.'
    }]


@pytest.fixture
def username():
    return 'username'


@pytest.fixture
def repo(username):
    return f'{username}/project'


@pytest.fixture
def commits1_output(commits1_items):
    return {'total_count': 1, 'incomplete_results': False, 'items': commits1_items}


@pytest.fixture
def url_page1():
    return 'https://api.github.com/search/commits?q=author:desecho+repo:desecho/movies+sort:author-date-desc&per_page=100&page=1'


@pytest.fixture
def url_page2():
    return 'https://api.github.com/search/commits?q=author:desecho+repo:desecho/movies+sort:author-date-desc&per_page=100&page=2'


@pytest.fixture
def commits2_output_page1(commits2_items_page1):
    return {'total_count': 101, 'incomplete_results': False, 'items': commits2_items_page1}


@pytest.fixture
def commits2_output_page2(commits2_items_page2):
    return {'total_count': 101, 'incomplete_results': False, 'items': commits2_items_page2}


@pytest.fixture
def github_mock():
    return flexmock(spec=github.Github)


@pytest.fixture
def requests_mock():
    return flexmock(spec=requests)


@pytest.fixture
def ghcontrib_github_mock():
    return flexmock(spec=Github)


@pytest.fixture
def user_mock():
    return flexmock()


@pytest.fixture
def repo_mock():
    repo = flexmock()
    repo.owner = flexmock()
    repo.owner.login = '123'
    return repo


@pytest.fixture
def gh():
    return Github()
