import os
import pytest
# local modules
from all_repos_add_readme.constants import Constants
from all_repos_add_readme.constants import GithubConstants
from all_repos_add_readme.constants import ToolArgumentNames


def test_tool_disclaimer_markdown() -> None:
    assert Constants.TOOL_GITHUB_REPO_URL in Constants.TOOL_DISCLAIMER_MD


def test_config_file_exists() -> None:
    assert os.path.isfile(GithubConstants.GITHUB_CONFIG_FILE.value)


def test_gen_argument_name_unsupported_how_arg() -> None:
    with pytest.raises(ValueError):
        ToolArgumentNames.gen_argument_name(ToolArgumentNames.README_FILE_ARGUMENT, how='bad input')
