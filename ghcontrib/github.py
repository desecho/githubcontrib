import github
import requests
from dateutil import parser
from django.conf import settings
from github.GithubException import UnknownObjectException


class Github:
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

    def get_commit_data(self, username: str, repo: str):
        if not self.repo_exists(repo):
            return None
        url = (f'https://api.github.com/search/commits?access_token={settings.GITHUB_API_KEY}&'
               f'q=author:{username}+repo:{repo}+sort:author-date-desc')
        r = requests.get(url, headers={'Accept': 'application/vnd.github.cloak-preview'})
        commits = r.json()['items']
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
