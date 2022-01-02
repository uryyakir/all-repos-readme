from typing_extensions import Literal
from typing import Tuple
from typing import Any
from git import Repo
import os
from enum import Enum
# local modules
from all_repos_add_readme.constants import GithubConstants


class GitConstants(Enum):
    CONFIG_LEVEL: Literal['repository'] = 'repository'
    API_KEY_CONFIG_SECTION = 'user'
    API_KEY_CONFIG_PROPERTY = (API_KEY_CONFIG_SECTION, GithubConstants.API_KEY.value)


class _Git:
    def __init__(self, directory: str = os.getcwd()):
        self._directory = directory
        self._repo = Repo.init(self._directory)


class GitConfigHandler(_Git):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

    def __getitem__(self, item: Tuple[str, str]) -> str:
        ret = self._repo.config_reader(config_level=GitConstants.CONFIG_LEVEL.value).get_value(*item)
        assert isinstance(ret, str)
        return ret

    def __setitem__(self, key: Tuple[str, str], value: str) -> None:
        self._repo.config_writer(config_level=GitConstants.CONFIG_LEVEL.value).set_value(*key, value).release()
        return

    def __delitem__(self, key: str) -> bool:
        _writer = self._repo.config_writer(config_level=GitConstants.CONFIG_LEVEL.value)
        is_deleted = _writer.remove_section(key)
        _writer.release()
        return is_deleted


git_config = GitConfigHandler()
