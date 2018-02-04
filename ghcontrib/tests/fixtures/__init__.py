import datetime

from dateutil.tz import tzoffset

from .commit_items import (
    commits1_items,
    commits2_items_page1,
    commits2_items_page2,
)

commits_jieter = [{
    'url': 'https://github.com/jieter/django-tables2/commit/360b29c5948c1f9bada618c30897e380e21a4f0a',
    'date': datetime.datetime(2017, 3, 6, 13, 30, 58, tzinfo=tzoffset(None, 3600)),
    'message': 'Regression fix - revert commit 05d8d1d260fe1cfe61a89ef0ae09c78513022f3c (#423)'
}]
commits_python_social_auth = [{
    'url':
    'https://github.com/python-social-auth/social-core/commit/ab19dc49a5366ae4f917bed2a7bfddce7e7b003f',
    'date':
    datetime.datetime(2017, 4, 16, 4, 39, 32, tzinfo=tzoffset(None, -14400)),
    'message':
    'Speed up authorization process for VKAppOAuth2\nUse first api request provided immediately instead of creating a new one.'
}]

username = 'user'
repo = f'{username}/project'
commits1_output = {'total_count': 1, 'incomplete_results': False, 'items': commits1_items}

url_page1 = 'https://api.github.com/search/commits?access_token=token&q=author:desecho+repo:desecho/movies+sort:author-date-desc&per_page=100&page=1'
url_page2 = 'https://api.github.com/search/commits?access_token=token&q=author:desecho+repo:desecho/movies+sort:author-date-desc&per_page=100&page=2'
commits2_output_page1 = {'total_count': 101, 'incomplete_results': False, 'items': commits2_items_page1}
commits2_output_page2 = {'total_count': 101, 'incomplete_results': False, 'items': commits2_items_page2}
