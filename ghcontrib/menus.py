# -*- coding: utf-8 -*-

from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from menu import Menu, MenuItem


def is_authenticated(request):
    return request.user.is_authenticated()


Menu.add_item('main', MenuItem(_('My Repos'), reverse('my_repos'), check=is_authenticated))
Menu.add_item('main', MenuItem(_('My Repos (Edit)'), reverse('my_repos_edit'), check=is_authenticated))
