"""GitHub."""
import github
from django.conf import settings
from github.GithubException import UnknownObjectException

from .types import CommitType


class Github:
    """GitHub."""

    # The limit is set by GitHub
    MAX_NUMBER_OF_ITEMS = 100

    def __init__(self) -> None:
        """Initialize GitHub."""
        self.gh = github.Github(settings.GITHUB_API_KEY, per_page=self.MAX_NUMBER_OF_ITEMS)

    def get_stars_count(self, username: str) -> int:
        """Get stars count."""
        stars = 0
        user = self.gh.get_user(username)
        repos = user.get_repos()
        for repo in repos:
            stars += repo.stargazers_count
        return stars

    def is_repo_exists(self, repo_name: str) -> bool:
        """Return True if repo exists."""
        username, repo_name = repo_name.split("/")
        user = self.gh.get_user(username)
        try:
            repo = user.get_repo(repo_name)
            if repo.owner.login != username:
                return False
        except UnknownObjectException:
            return False
        return True

    def get_commit_data(self, username: str, repo: str) -> list[CommitType]:
        """Get commit data."""
        commits = self.gh.search_commits("", "author-date", "desc", author=username, repo=repo)
        commit_data: list[CommitType] = []
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
