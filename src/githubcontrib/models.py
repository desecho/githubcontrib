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
    TextField,
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

    def fetch_stars(self, save: bool = True) -> None:
        """Fetch stars."""
        gh = Github()
        stars = gh.get_stars_count(self.username)
        self.stars = stars
        if save:
            self.save()


class Repo(Model):
    """Repo."""

    user = ForeignKey(User, CASCADE, related_name="repos")
    name = CharField(max_length=255)

    def __str__(self) -> str:
        """Return string representation."""
        return str(self.name)

    class Meta:
        """Meta."""

        ordering = ["name"]


class Commit(Model):
    """Commit."""

    repo = ForeignKey(Repo, CASCADE, related_name="commits")
    url = URLField()
    date = DateTimeField()
    message = TextField()

    def __str__(self) -> str:
        """Return string representation."""
        return f"{self.repo} - {self.message}"

    class Meta:
        """Meta."""

        ordering = ["-date"]
