from github import Github
from typing import NamedTuple


class GithubConfig(NamedTuple):
    username: str
    api_key: str
