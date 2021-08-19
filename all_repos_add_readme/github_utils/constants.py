from enum import Enum


TOOL_NAME = "all_repos_add_readme"
TOOL_COMMIT_MESSAGE = "add README.md (automatically committed by the `all_repos_add_readme` tool)"
TOOL_DISCLAIMER_MD = """#### Disclaimer: this is an auto-generated README.md file, committed by the [{tool_name}](https://github.com/uryyakir/all-repos-readme) tool at {current_date}.
To update repo stats, re-run the tool :)"""


class GithubConstants(Enum):
    API_KEY = "apiKey"
    USERNAME = "username"
    GITHUB_CONFIG_FILE = "config.json"


class GitConstants:
    CONFIG_LEVEL = "repository"
    API_KEY_CONFIG_SECTION = "user"
    API_KEY_CONFIG_PROPERTY = (API_KEY_CONFIG_SECTION, GithubConstants.API_KEY.value)
