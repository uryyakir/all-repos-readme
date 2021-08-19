from enum import Enum


TOOL_NAME = "all_repos_add_readme"


class GithubConstants(Enum):
    API_KEY = "apiKey"
    USERNAME = "username"
    GITHUB_CONFIG_FILE = "config.json"


class GitConstants:
    CONFIG_LEVEL = "repository"
    API_KEY_CONFIG_SECTION = "user"
    API_KEY_CONFIG_PROPERTY = (API_KEY_CONFIG_SECTION, GithubConstants.API_KEY.value)
