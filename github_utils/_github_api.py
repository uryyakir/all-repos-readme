from github import Github
from typing import NamedTuple


class GithubConfig(NamedTuple):
    username: str
    apiKey: str
