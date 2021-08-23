import pytest
from github import Github
from github.Repository import Repository
from github.Commit import Commit
import json
from typing import Type
import datetime as dt
# local modules
from all_repos_add_readme.constants import GithubConstants
from all_repos_add_readme.constants import TOOL_NAME
from all_repos_add_readme.constants import TOOL_DISCLAIMER_MD
from all_repos_add_readme.github_utils._github_repo import _Repo  # noqa
from all_repos_add_readme.github_utils.git_utils import GitConfigHandler


@pytest.fixture
def get_github_repository_object() -> Repository:
    with open(GithubConstants.GITHUB_CONFIG_FILE.value, 'r', encoding='utf-8') as config_file:
        _config = json.load(config_file)

    return Github(login_or_token=_config[GithubConstants.API_KEY.value]).get_repo(full_name_or_id="uryyakir/all-repos-readme-testing")


@pytest.fixture
def get_repo_object(get_github_repository_object: Repository) -> _Repo:
    return _Repo(get_github_repository_object)


def get_last_commit(get_github_repository_object: Repository) -> Commit:
    return list(get_github_repository_object.get_commits())[0]


github_config_handler = GitConfigHandler()


@pytest.fixture
def git_config_handler_object() -> GitConfigHandler:
    return github_config_handler  # return a reference instead of reinitializing for every test function


class Constants:
    # test_repo_ignore.py constants
    TEST_AGAINST_USERNAME = "uryyakir"
    TEST_AGAINST_REPO_NAME = "all-repos-readme-testing"
    # test_github_repo.py constants
    TEST_MARKDOWN_FILE_PATH = "all_repos_add_readme/github_utils/tests/test_markdown.md"
    TOOL_TEST_STRING = "some string"
    TOOL_SIGNATURE_STRING = TOOL_DISCLAIMER_MD.format(tool_name=TOOL_NAME, current_date=dt.datetime.today().strftime("%d/%m/%Y"))
    # test_git_utils.py constants
    TEST_SECTION_NAME = "testSectionName"
    TEST_PROPERTY_NAME = "testPropertyName"
    TEST_PROPERTY_VALUE = "test_property_value"
    TEST_PROPERTY_PATH = (TEST_SECTION_NAME, TEST_PROPERTY_NAME)
    # test_github_api constants
    TEST_CUSTOM_COMMIT_MESSAGE = "test commit message"
    ONLY_TEST_AGAINST_REPO_FILTER = (rf"(?!.*({TEST_AGAINST_REPO_NAME}))",)
    TEST_USER_INPUT = "some markdown string input"
    # test_logger constants
    LOGFILES_ITERATION_COUNTER = 2
    CUSTOM_LOGFILE_NAME = "some_logfile_name"
    # test_main constants
    CUSTOM_README_STRING = """
# # some string
# ## some other string
# <ul>
#     <li>item1</li>
#     <li>item12</li>
# </ul>
#
"""


@pytest.fixture
def constants() -> Type[Constants]:
    return Constants
