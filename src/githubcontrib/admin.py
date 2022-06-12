from django.contrib.admin import site
from django.contrib.auth.models import Group
from social_django.models import Association, Nonce

from .models import Commit, Repo, User

site.register(User)
site.register(Repo)
site.register(Commit)


site.unregister(Nonce)
site.unregister(Association)
site.unregister(Group)
