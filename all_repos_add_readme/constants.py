from typing import Tuple
from enum import Enum
from time import time
import os


TOOL_NAME = "all_repos_readme"
TOOL_CLI_DESCRIPTION = "A tool to create a generic README.md for all of the user's owned REPOs.\n"
"One can either provide a local readme-file (-rf) or provide a MD-formatted string (-rs).\n"
"The provided input will be added to all of the user's owned REPOs that don't already have a readme file.\n"
"If no input is provided, the tool will generate an automated README file for all REPOs.\n"
"You can find the README default template under all_repos_add_readme/readme_template.md"
TOOL_GITHUB_REPO_URL = "https://github.com/uryyakir/all-repos-readme"
TOOL_COMMIT_SIGNATURE = " (automatically committed by the `all_repos_readme` tool)"
TOOL_COMMIT_MESSAGE = "add README.md" + TOOL_COMMIT_SIGNATURE
TOOL_DISCLAIMER_MD = f"""#### Disclaimer: this is an auto-generated README.md file, committed by the [{{tool_name}}]({TOOL_GITHUB_REPO_URL}) tool at {{current_date}}.
To update repo stats, re-run the tool :)"""
README_TEMPLATE_FILE_NAME = "readme_template.md"
TOOL_README_TEMPLATE_PATH = os.path.join("all_repos_add_readme", README_TEMPLATE_FILE_NAME)


class ToolArgumentNames:
    README_FILE_ARGUMENT = "readme_file"
    README_STRING_ARGUMENT = "readme_string"
    USER_INPUT_ARGUMENT = "user_input"
    VERBOSE_ARGUMENT = "verbose"
    DRY_RUN_ARGUMENT = "dry_run"
    COMMIT_MESSAGE_ARGUMENT = "commit_message"
    LOG_TO_FILE_ARGUMENT = "log_to_file"

    def __getattr__(self, item: str) -> str:
        argument_name = (ToolArgumentNames.__dict__[item.upper() + "_ARGUMENT"]).replace("_", "-")
        return argument_name

    @staticmethod
    def _gen_full_arg_name(_arg_name: str) -> str:
        return "--" + _arg_name

    @staticmethod
    def _gen_abbrev_arg_name(_arg_name: str) -> str:
        return "-" + "".join([word[0] for word in _arg_name.split("-")])

    @staticmethod
    def gen_argument_name(item: str, how: str) -> Tuple[str, ...]:
        assert how in ('only full', 'only abbrev', 'both')
        _arg_name = ToolArgumentNames().__getattr__(item)

        if how == 'both':
            return ToolArgumentNames._gen_full_arg_name(_arg_name), ToolArgumentNames._gen_abbrev_arg_name(_arg_name)

        elif how == 'only full':
            return (ToolArgumentNames._gen_full_arg_name(_arg_name),)

        elif how == 'only abbrev':
            return (ToolArgumentNames._gen_abbrev_arg_name(_arg_name),)

        else:
            raise NotImplementedError()


class LoggerConstants:
    # log constants
    TOOL_LOGGER_NAME = "logger"
    TOOL_DEFAULT_LOGFILE_DIR = "logs"
    ROTATING_FILE_HANDLER_BACKUP_COUNT = 5

    @property
    def tool_default_logfile_name(self) -> str:
        return f"logfile_{round(time())}.log"


class GithubConstants(Enum):
    API_KEY = "apiKey"
    USERNAME = "username"
    GITHUB_CONFIG_FILE = "config.json"


class GitConstants(Enum):
    CONFIG_LEVEL = "repository"
    API_KEY_CONFIG_SECTION = "user"
    API_KEY_CONFIG_PROPERTY = (API_KEY_CONFIG_SECTION, GithubConstants.API_KEY.value)


class LoggerColoring(Enum):
    GREEN = "\x1b[32m"
    RESET_SEQ = "\033[0m"
