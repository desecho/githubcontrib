from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    homepage = models.URLField(blank=True, null=True)


class Repo(models.Model):
    user = models.ForeignKey(User, models.CASCADE, related_name='repos')
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Commit(models.Model):
    repo = models.ForeignKey(Repo, models.CASCADE, related_name='commits')
    url = models.URLField()
    date = models.DateTimeField()
    message = models.CharField(max_length=255)

    def __str__(self):
        return self.message
