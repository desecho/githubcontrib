import json

from django.urls import reverse

from .base import BaseTestLoginCase


class GithubContribHomeTestCase(BaseTestLoginCase):
    def test_home(self):
        url = reverse('home')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertListEqual(list(response.context_data['usernames']), ['fox', 'ironman'])

    def test_home_anonymous(self):
        self.client.logout()
        url = reverse('home')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertListEqual(list(response.context_data['usernames']), ['fox', 'ironman', 'neo'])


class GithubContribContributionsTestCase(BaseTestLoginCase):
    """
    Dumpdata commands:
    manage dumpdata ghcontrib.Repo --indent 4 > ghcontrib/fixtures/repos.json
    manage dumpdata ghcontrib.Commit --indent 4 > ghcontrib/fixtures/commits.json

    User actions in fixtures:
    neo:
        - Added jieter/django-tables2
        - Added python-social-auth/social-core
        - Loaded commit data
    """

    fixtures = [
        'users.json',
        'repos.json',
        'commits.json',
    ]

    def contribs(self, page, with_username=True, status_code=200):
        username = 'neo'
        args = (username, ) if with_username else None
        url = reverse(page, args=args)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status_code)
        if status_code == 302:
            response = self.client.get(url, follow=True)
        repos = list(response.context_data['repos'].values_list('pk', flat=True))
        self.assertListEqual(repos, [1, 2])
        self.assertEqual(response.context_data['username'], username)

    def test_contribs(self):
        self.contribs('contribs')

    def test_contribs_anonymous(self):
        self.client.logout()
        self.contribs('contribs')

    def test_my_contribs(self):
        self.contribs('my_contribs', False, 302)

    def test_contribs_not_found(self):
        url = reverse('contribs', args=('potato', ))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_my_repos(self):
        url = reverse('my_repos')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        repos = json.loads(response.context_data['repos'])
        self.assertListEqual(repos, [{
            'id': 1,
            'name': 'jieter/django-tables2'
        }, {
            'id': 2,
            'name': 'python-social-auth/social-core'
        }])
