"""ghcontrib_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth.views import login
# from django.views.i18n import javascript_catalog
from ghcontrib.views.user import logout_view, PreferencesView
from ghcontrib.views.ghcontrib import (HomeView, ReposView, MyReposView, MyReposEditView, AddRepoView,
                                       DeleteRepoView, LoadCommitDataView)


admin.autodiscover()

urlpatterns = [
    url(r'^$', HomeView.as_view(), name='home'),

    # User
    url(r'^login/$', login, {'template_name': 'user/login.html'}, name='login'),
    url(r'^logout/$', logout_view, name='logout'),
    # -= Preferences =-
    url(r'^preferences/$', PreferencesView.as_view(), name='preferences'),

    url(r'^admin/', include(admin.site.urls)),

    # Services
    # url(r'^jsi18n/$', javascript_catalog, {
    #     'domain': 'djangojs',
    #     'packages': ('movies',)}, name='javascript-catalog'),

    url('', include('social_django.urls', namespace='social')),
    # url(r'^rosetta/', include('rosetta.urls')),
    # url(r'^i18n/', include('django.conf.urls.i18n')),
    url(r'^my-repos/edit/$', MyReposEditView.as_view(), name='my_repos_edit'),
    url(r'^delete-repo/$', DeleteRepoView.as_view(), name='delete_repo'),
    url(r'^add-repo/$', AddRepoView.as_view(), name='add_repo'),
    url(r'^my-repos/$', MyReposView.as_view(), name='my_repos'),
    url(r'^load-commit-data/$', LoadCommitDataView.as_view(), name='load_commit_data'),
    url(r'^(?P<username>[\w\d_-]+)/$', ReposView.as_view(), name='repos'),

]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]
