"""Models."""
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db.models import (
    CASCADE,
    BooleanField,
    CharField,
    DateTimeField,
    ForeignKey,
    Model,
    PositiveIntegerField,
    PositiveSmallIntegerField,
    TextField,
    UniqueConstraint,
    URLField,
)

from .github import Github


class User(AbstractUser):
    """User."""

    language = CharField(max_length=2, choices=settings.LANGUAGES, default=settings.LANGUAGE_CODE)
    avatar = URLField(null=True, blank=True)
    loaded_initial_data = BooleanField(default=False)
    stars = PositiveIntegerField(default=0)

    @property
    def github_profile_url(self) -> str:
        """Return GitHub profile URL."""
        return f"https://github.com/{self.username}"

    def fetch_stars(self) -> int:
        """Fetch stars."""
        gh = Github()
        return gh.get_stars_count(self.username)


class Repo(Model):
    """Repo."""

    user = ForeignKey(User, CASCADE, related_name="repos")
    name = CharField(max_length=255)
    order = PositiveSmallIntegerField(default=0)

    def __str__(self) -> str:
        """Return string representation."""
        return f"{self.user} - {self.name}"

    class Meta:
        """Meta."""

        ordering = ["order", "name"]
        constraints = [
            # A user should not have duplicated repos
            UniqueConstraint(fields=("user", "name"), name="unique_user_name_repo"),
        ]


class Commit(Model):
    """Commit."""

    repo = ForeignKey(Repo, CASCADE, related_name="commits")
    url = URLField(unique=True)
    date = DateTimeField()
    message = TextField()

    def __str__(self) -> str:
        """Return string representation."""
        return f"{self.repo} - {self.message}"

    class Meta:
        """Meta."""

        ordering = ["-date"]
