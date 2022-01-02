from enum import Enum
from github.GithubException import UnknownObjectException

# local modules
from all_repos_add_readme.constants import ToolArgumentNames


class InvalidReadme(BaseException):
    def __init__(self, message: str) -> None:
        super().__init__(message)


class RepoReadmeNeedsUpdate(UnknownObjectException):
    def __init__(self, readme_sha: str) -> None:
        super().__init__('', '', {})
        self.sha = readme_sha


class ExceptionMessages(Enum):
    BOTH_STDIN_AND_FILE = 'both a readme-string and a readme-file were provided. Please make sure you only provide one!'
    NONE_PROVIDED = 'neither a readme-string nor a readme-file were provided. Please make sure you provide one!'
    _REPOIGNORE_FILEPATH_ARGUMENT = ToolArgumentNames.gen_argument_name(
        ToolArgumentNames.REPOIGNORE_FILEPATH_ARGUMENT, how='only full',
    )[0]
    NO_REPOIGNORE_FILE_WARNING = f"""Note: no .repoignore file found in your current working directory.
This file can be leveraged to have a finer control of the affected repositories.
If you have a .repoignore file located somewhere in your FS, you may provide its exact path using the `{_REPOIGNORE_FILEPATH_ARGUMENT}`
CLI parameter.
"""
