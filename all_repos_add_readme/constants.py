from enum import Enum


TOOL_NAME = "all_repos_readme"
TOOL_CLI_DESCRIPTION = "A tool to create a generic README.md for all of the user's owned REPOs.\n"
"One can either provide a local readme-file (-rf) or provide a MD-formatted string (-rs).\n"
"The provided input will be added to all of the user's owned REPOs that don't already have a readme file.\n"
"If no input is provided, the tool will generate an automated README file for all REPOs.\n"
"You can find the README default template under all_repos_add_readme/readme_template.md"
TOOL_COMMIT_MESSAGE = "add README.md (automatically committed by the `all_repos_add_readme` tool)"
TOOL_DISCLAIMER_MD = """#### Disclaimer: this is an auto-generated README.md file, committed by the [{tool_name}](https://github.com/uryyakir/all-repos-readme) tool at {current_date}.
To update repo stats, re-run the tool :)"""


class GithubConstants(Enum):
    API_KEY = "apiKey"
    USERNAME = "username"
    GITHUB_CONFIG_FILE = "config.json"


class GitConstants(Enum):
    CONFIG_LEVEL = "repository"
    API_KEY_CONFIG_SECTION = "user"
    API_KEY_CONFIG_PROPERTY = (API_KEY_CONFIG_SECTION, GithubConstants.API_KEY.value)
