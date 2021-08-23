import pytest
from github import Github
from github.Repository import Repository
import json
from typing import Type
import datetime as dt
# local modules
from all_repos_add_readme.constants import GithubConstants
from all_repos_add_readme.constants import TOOL_NAME
from all_repos_add_readme.constants import TOOL_DISCLAIMER_MD
from all_repos_add_readme.github_utils._github_repo import _Repo  # noqa


@pytest.fixture
def get_github_repository_object() -> Repository:
    with open("config.json", 'r', encoding='utf-8') as config_file:
        _config = json.load(config_file)

    return Github(login_or_token=_config[GithubConstants.API_KEY.value]).get_repo(full_name_or_id="uryyakir/all-repos-readme-testing")


@pytest.fixture
def get_repo_object(get_github_repository_object: Repository) -> _Repo:
    return _Repo(get_github_repository_object)


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


@pytest.fixture
def constants() -> Type[Constants]:
    return Constants
