from django.contrib.admin import site

from .models import Commit, Repo, User

site.register(User)
site.register(Repo)
site.register(Commit)
