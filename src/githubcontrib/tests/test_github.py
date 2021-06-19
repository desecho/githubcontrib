# from flexmock import flexmock
# from github.GithubException import UnknownObjectException

# pylint: disable=no-name-in-module


# def test_repo_exists_wrong_user(repo, github_mock, gh):
#     github_mock.should_receive("get_user").and_raise(UnknownObjectException(None, None))
#     result = gh.repo_exists(repo)
#     assert result is False


# def test_repo_exists_wrong_repo(repo, github_mock, user_mock, gh):
#     github_mock.should_receive("get_user").and_return(user_mock)
#     user_mock.should_receive("get_repo").and_raise(UnknownObjectException(None, None))
#     result = gh.repo_exists(repo)
#     assert result is False


def test_repo_exists_user_mismatch(repo, github_mock, user_mock, repo_mock, gh):
    github_mock.should_receive("get_user").and_return(user_mock)
    user_mock.should_receive("get_repo").and_return(repo_mock)
    result = gh.repo_exists(repo)
    assert result is False


def test_repo_exists_success(repo, username, github_mock, user_mock, repo_mock, gh):
    github_mock.should_receive("get_user").and_return(user_mock)
    repo_mock.owner.login = username
    user_mock.should_receive("get_repo").and_return(repo_mock)
    result = gh.repo_exists(repo)
    assert result is True


# def test_load_commits_one_page(
#     githubcontrib_github_mock,
#     gh,
#     commits1_items,
#     repo,
#     commits1_output,
#     username,
#     requests_mock,
# ):
#     githubcontrib_github_mock.should_receive("repo_exists").and_return(True)
#     response_mock = flexmock()
#     response_mock.should_receive("json").and_return(commits1_output)
#     requests_mock.should_receive("get").and_return(response_mock)
#     result = gh._load_commits(username, repo, 1, [])  # pylint: disable=protected-access
#     assert result == commits1_items


# def test_load_commits_two_pages(
#     commits2_items_total,
#     url_page1,
#     url_page2,
#     commits2_output_page1,
#     gh,
#     commits2_output_page2,
#     requests_mock,
#     githubcontrib_github_mock,
# ):
#     githubcontrib_github_mock.should_receive("repo_exists").and_return(True)
#     response_mock_page1 = flexmock()
#     response_mock_page1.should_receive("json").and_return(commits2_output_page1)
#     requests_mock.should_receive("get").with_args(
#         url_page1, headers=gh.HEADERS
#     ).and_return(response_mock_page1)
#     response_mock_page2 = flexmock()
#     response_mock_page2.should_receive("json").and_return(commits2_output_page2)
#     requests_mock.should_receive("get").with_args(
#         url_page2, headers=gh.HEADERS
#     ).and_return(response_mock_page2)

#     result = gh._load_commits(
#         "desecho", "desecho/movies", 1, []
#     )  # pylint: disable=protected-access
#     assert result == commits2_items_total


def test_get_commit_data_fail(repo, username, githubcontrib_github_mock, gh):
    githubcontrib_github_mock.should_receive("repo_exists").and_return(False)
    result = gh.get_commit_data(username, repo)
    assert result is None


def test_get_commit_data_success(
    repo,
    username,
    githubcontrib_github_mock,
    commits1_items,
    commits_python_social_auth,
    gh,
):
    githubcontrib_github_mock.should_receive("repo_exists").and_return(True)
    githubcontrib_github_mock.should_receive("_load_commits").and_return(commits1_items)
    result = gh.get_commit_data(username, repo)
    assert result == commits_python_social_auth
