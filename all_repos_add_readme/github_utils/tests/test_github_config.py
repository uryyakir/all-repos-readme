from all_repos_add_readme.constants import GithubConstants
from all_repos_add_readme.github_utils._github_config import _GithubConfig


def test_github_config_attrs() -> None:
    assert GithubConstants.API_KEY.value in _GithubConfig._fields
