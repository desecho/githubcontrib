from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    language = models.CharField(max_length=2, choices=settings.LANGUAGES, default=settings.LANGUAGE_CODE)
    avatar = models.URLField(null=True, blank=True)
    loaded_initial_data = models.BooleanField(default=False)

    @property
    def github_profile_url(self) -> str:
        return f"https://github.com/{self.username}"


class Repo(models.Model):
    user = models.ForeignKey(User, models.CASCADE, related_name="repos")
    name = models.CharField(max_length=255)

    def __str__(self):
        return str(self.name)

    class Meta:
        ordering = ["name"]


class Commit(models.Model):
    repo = models.ForeignKey(Repo, models.CASCADE, related_name="commits")
    url = models.URLField()
    date = models.DateTimeField()
    message = models.TextField()

    def __str__(self) -> str:
        return f"{self.repo} - {self.message}"

    class Meta:
        ordering = ["-date"]
