from typing import Any, Dict, List

import github
from django.conf import settings
from github.Commit import Commit
from github.GithubException import UnknownObjectException
from github.PaginatedList import PaginatedList


class Github:
    # The limit is set by GitHub
    MAX_NUMBER_OF_ITEMS = 100

    def __init__(self) -> None:
        self.gh = github.Github(settings.GITHUB_API_KEY, per_page=self.MAX_NUMBER_OF_ITEMS)

    def repo_exists(self, repo_name: str) -> bool:
        username, repo_name = repo_name.split("/")
        try:
            user = self.gh.get_user(username)
        except UnknownObjectException:
            return False
        try:
            repo = user.get_repo(repo_name)
            if repo.owner.login != username:
                return False
        except UnknownObjectException:
            return False
        return True

    def _load_commits(
        self,
        commits_paginated: PaginatedList,  # type: ignore
        page: int,
        commits_total: List[Commit],
    ) -> List[Commit]:
        commits = commits_paginated.get_page(page)
        commits_total += commits
        if len(commits) == self.MAX_NUMBER_OF_ITEMS:
            return self._load_commits(commits_paginated, page + 1, commits_total)
        return commits_total

    def get_commit_data(self, username: str, repo: str) -> List[Dict[str, Any]]:
        commits_paginated = self.gh.search_commits("", "author-date", "desc", author=username, repo=repo)
        commits = self._load_commits(commits_paginated, 0, [])
        commit_data = []
        for commit in commits:
            commit_git = commit.commit
            commit_data.append(
                {
                    "url": commit_git.html_url,
                    "date": commit_git.committer.date,
                    "message": commit_git.message,
                }
            )
        return commit_data
