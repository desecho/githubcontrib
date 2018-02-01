from django.contrib import admin

from .models import Commit, Repo, User

admin.site.register(User)
admin.site.register(Repo)
admin.site.register(Commit)
