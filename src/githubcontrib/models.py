from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db.models import CASCADE, BooleanField, CharField, DateTimeField, ForeignKey, Model, TextField, URLField


class User(AbstractUser):
    language = CharField(max_length=2, choices=settings.LANGUAGES, default=settings.LANGUAGE_CODE)
    avatar = URLField(null=True, blank=True)
    loaded_initial_data = BooleanField(default=False)

    @property
    def github_profile_url(self) -> str:
        return f"https://github.com/{self.username}"


class Repo(Model):
    user = ForeignKey(User, CASCADE, related_name="repos")
    name = CharField(max_length=255)

    def __str__(self) -> str:
        return str(self.name)

    class Meta:
        ordering = ["name"]


class Commit(Model):
    repo = ForeignKey(Repo, CASCADE, related_name="commits")
    url = URLField()
    date = DateTimeField()
    message = TextField()

    def __str__(self) -> str:
        return f"{self.repo} - {self.message}"

    class Meta:
        ordering = ["-date"]
