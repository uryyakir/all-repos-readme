from typing import Tuple
from typing import Any
from git import Repo
import os
# local modules
from all_repos_add_readme.github_utils.constants import GitConstants


class _Git:
    def __init__(self, directory: str = os.getcwd()):
        self._directory = directory
        self._repo = Repo.init(self._directory)


class GitConfigHandler(_Git):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super(GitConfigHandler, self).__init__(*args, **kwargs)

    def __getitem__(self, item: Tuple[str, str]) -> str:
        return self._repo.config_reader(config_level=GitConstants.CONFIG_LEVEL).get_value(*item)

    def __setitem__(self, key: Tuple[str, str], value: str) -> None:
        self._repo.config_writer(config_level=GitConstants.CONFIG_LEVEL).set_value(*key, value).release()
        return

    def __delitem__(self, key: Tuple[str, str]) -> None:
        self._repo.config_writer(config_level=GitConstants.CONFIG_LEVEL).remove_section(GitConstants.API_KEY_CONFIG_SECTION)
        return


git_config = GitConfigHandler()
