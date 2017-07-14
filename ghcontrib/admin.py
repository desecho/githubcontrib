from django.contrib import admin

from .models import User, Repo, Commit


admin.site.register(User)
admin.site.register(Repo)
admin.site.register(Commit)
