import github
from django.conf import settings
from github.GithubException import UnknownObjectException


class Github:
    # The limit is set by GitHub
    MAX_NUMBER_OF_ITEMS = 100

    def __init__(self):
        self.gh = github.Github(settings.GITHUB_API_KEY, per_page=self.MAX_NUMBER_OF_ITEMS)

    def repo_exists(self, repo: str) -> bool:
        username, repo = repo.split("/")
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

    def _load_commits(self, commits_paginated, page, commits_total):
        commits = commits_paginated.get_page(page)
        commits_total += commits
        if len(commits) == self.MAX_NUMBER_OF_ITEMS:
            return self._load_commits(commits_paginated, page + 1, commits_total)
        return commits_total

    def get_commit_data(self, username: str, repo: str):
        commits = self.gh.search_commits("", "author-date", "desc", author=username, repo=repo)
        commits = self._load_commits(commits, 0, [])
        commit_data = []
        for commit in commits:
            commit = commit.commit
            commit_data.append(
                {
                    "url": commit.html_url,
                    "date": commit.committer.date,
                    "message": commit.message,
                }
            )
        return commit_data
