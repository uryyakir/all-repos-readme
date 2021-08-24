import os
# local modules
from all_repos_add_readme.constants import TOOL_GITHUB_REPO_URL
from all_repos_add_readme.constants import TOOL_DISCLAIMER_MD
from all_repos_add_readme.constants import GithubConstants


def test_tool_disclaimer_markdown() -> None:
    assert TOOL_GITHUB_REPO_URL in TOOL_DISCLAIMER_MD


def test_config_file_exists() -> None:
    assert os.path.isfile(GithubConstants.GITHUB_CONFIG_FILE.value)
