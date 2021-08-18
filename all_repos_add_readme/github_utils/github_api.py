from typing import NamedTuple
from argparse import Namespace
from github import Github
from github.GithubException import UnknownObjectException
import json
# local modules


class GithubConfig(NamedTuple):
    username: str
    apiKey: str


def main(res: Namespace) -> None:
    with open('config.json', encoding='utf8') as config_file:
        github_config = GithubConfig(**json.load(config_file))

    github = Github(login_or_token=github_config.apiKey)
    for repo in set(github.get_user().get_repos(affiliation='owner')):
        if not repo.fork:
            try:
                print(f"{repo.name}: {repo.get_readme()})")
            except UnknownObjectException:
                print(f"{repo.name}: error!")


if __name__ == "__main__":
    # some random input for testing purposes
    main(
        Namespace(readme_file=None, readme_string=["some_string"])
    )
