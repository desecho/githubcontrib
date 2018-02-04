from django.contrib.auth.models import AbstractUser
from django.contrib.auth.signals import user_logged_in
from django.db import models
from django.dispatch import receiver
from django.utils.translation import LANGUAGE_SESSION_KEY
from django.conf import settings


def activate_user_language_preference(request, lang):
    request.session[LANGUAGE_SESSION_KEY] = lang


class User(AbstractUser):
    language = models.CharField(max_length=2, choices=settings.LANGUAGES, default='en')


class Repo(models.Model):
    user = models.ForeignKey(User, models.CASCADE, related_name='repos')
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Commit(models.Model):
    repo = models.ForeignKey(Repo, models.CASCADE, related_name='commits')
    url = models.URLField()
    date = models.DateTimeField()
    message = models.CharField(max_length=255)

    def __str__(self):
        return self.message

    class Meta:
        ordering = ['-date']


@receiver(user_logged_in)
def lang(**kwargs):
    activate_user_language_preference(kwargs['request'], kwargs['user'].language)
