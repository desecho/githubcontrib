import json

from django.urls import reverse
from flexmock import flexmock

from ghcontrib.github import Github
from ghcontrib.models import Commit

from .base import BaseTestLoginCase
from .fixtures import commits_jieter, commits_python_social_auth, repo


class ContribHomeTestCase(BaseTestLoginCase):
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


class ContributionsTestCase(BaseTestLoginCase):
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


class ReposTestCase(BaseTestLoginCase):
    fixtures = [
        'users.json',
        'repos.json',
    ]

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


class RepoTestCase(BaseTestLoginCase):
    fixtures = [
        'users.json',
        'repos.json',
    ]

    def setUp(self):
        super().setUp()
        self.github_mock = flexmock(spec=Github)
        self.url = reverse('repo')

    def test_add_repo_wrong_name(self):
        response = self.client.post(self.url, {'name': 'something'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.get_json(response), {'status': 'fail', 'error': 'Repository name is incorrect'})

    def test_add_repo_success(self):
        self.github_mock.should_receive('repo_exists').and_return(True)
        response = self.client.post(self.url, {'name': repo})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.get_json(response), {'status': 'success', 'id': 3})

    def test_add_repo_repo_not_found(self):
        self.github_mock.should_receive('repo_exists').and_return(False)
        response = self.client.post(self.url, {'name': repo})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.get_json(response), {'status': 'fail', 'error': 'Repository not found'})

    def test_add_repo_exists(self):
        self.github_mock.should_receive('repo_exists').and_return(True)
        response = self.client.post(self.url, {'name': 'jieter/django-tables2'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.get_json(response), {'error': 'Repository already exists', 'status': 'fail'})

    def test_delete_repo(self):
        url = reverse('delete_repo', args=(1, ))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.get_json(response), {'status': 'success'})
        repos = list(self.user.repos.all().values_list('pk', flat=True))
        self.assertListEqual(repos, [2])

    def test_delete_repo_does_not_exist(self):
        url = reverse('delete_repo', args=(5, ))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.get_json(response), {'status': 'fail', 'error': 'Repository not found'})

    def test_delete_repo_bad_request(self):
        url = reverse('repo')
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 400)


class LoadCommitDataTestCase(BaseTestLoginCase):
    fixtures = [
        'users.json',
        'repos.json',
    ]

    def setUp(self):
        super().setUp()
        self.github_mock = flexmock(spec=Github)
        self.url = reverse('load_commit_data')

    def test_load_commit_data_success(self):
        self.github_mock.should_receive('get_commit_data').with_args(
            'neo', 'jieter/django-tables2').and_return(commits_jieter)
        self.github_mock.should_receive('get_commit_data').with_args(
            'neo', 'python-social-auth/social-core').and_return(commits_python_social_auth)
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 200)
        commits = Commit.objects.filter(repo__user=self.user)
        self.assertListEqual(list(commits.values_list('pk', flat=True)), [2, 1])
        self.assertIn('python-social-auth/social-core', commits[0].url)
        self.assertIn('jieter/django-tables2', commits[1].url)

    def test_load_commit_data_repo_not_found(self):
        self.github_mock.should_receive('get_commit_data').and_return(None)
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            self.get_json(response), {
                'error': 'Repository jieter/django-tables2 not found',
                'status': 'fail'
            })


class LogoutTestCase(BaseTestLoginCase):
    def test_logout(self):
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(self.is_authenticated)


class PreferencesTestCase(BaseTestLoginCase):
    def test_preferences(self):
        response = self.client.get(reverse('preferences'))
        self.assertEqual(response.status_code, 200)

    def test_save_preferences(self):
        language = 'ru'
        response = self.client.post(reverse('save_preferences'), {'language': language})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.get_json(response), {'status': 'success'})
        User = self.get_user_model()
        user = User.objects.get(pk=self.user.pk)
        self.assertEqual(user.language, language)

    def test_save_preferences_bad_request(self):
        response = self.client.post(reverse('save_preferences'))
        self.assertEqual(response.status_code, 400)
