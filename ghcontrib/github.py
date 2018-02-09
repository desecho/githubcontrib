import urllib

import github
import requests
from dateutil import parser
from django.conf import settings
from github.GithubException import UnknownObjectException


class Github:
    # The limit is set by GitHub
    MAX_NUMBER_OF_ITEMS = 100
    BASE_URL = 'https://api.github.com'
    HEADERS = {'Accept': 'application/vnd.github.cloak-preview', 'Authorization': settings.GITHUB_API_KEY}

    def __init__(self):
        self.gh = github.Github(settings.GITHUB_API_KEY)

    def repo_exists(self, repo: str) -> bool:
        username, repo = repo.split('/')
        try:
            user = self.gh.get_user(username)
        except UnknownObjectException:
            return False
        try:
            repo = user.get_repo(repo)
            if repo.owner.login != username:
                return False
        except UnknownObjectException:
            return False
        return True

    def _load_commits(self, username, repo, page, commits_total):
        # Use sort filter here because we want to make sure we can use pagination consistently.
        params = {
            'q': f'author:{username}+repo:{repo}+sort:author-date-desc',
            'per_page': self.MAX_NUMBER_OF_ITEMS,
            'page': page,
        }
        params = urllib.parse.urlencode(params)
        params = urllib.parse.unquote(params)
        # We can't use requests' params argument because of this - https://github.com/requests/requests/issues/2701
        r = requests.get(f'{self.BASE_URL}/search/commits?{params}', headers=self.HEADERS)
        url = (f'{self.BASE_URL}/search/commits?access_token={settings.GITHUB_API_KEY}&'
               f'q=author:{username}+repo:{repo}+sort:author-date-desc&'
               f'per_page={self.MAX_NUMBER_OF_ITEMS}&page={page}')
        commits = r.json()['items']
        commits_total += commits
        if len(commits) == self.MAX_NUMBER_OF_ITEMS:
            return self._load_commits(username, repo, page + 1, commits_total)
        return commits_total

    def get_commit_data(self, username: str, repo: str):
        if not self.repo_exists(repo):
            return None
        commits = self._load_commits(username, repo, 1, [])
        commit_data = []
        for commit in commits:
            url = commit['html_url']
            date = commit['commit']['committer']['date']
            date = parser.parse(date)
            message = commit['commit']['message']
            commit_data.append({
                'url': url,
                'date': date,
                'message': message,
            })
        return commit_data
