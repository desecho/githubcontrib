from ghcontrib.github import Github

def load_user_data(backend, user, **kwargs):  # pylint: disable=unused-argument
    if user.loaded_initial_data:
        return None

    gh = Github().gh
    gh_user = gh.get_user(user.username)
    user.avatar = gh_user.avatar_url
    user.loaded_initial_data = True
    user.save()
