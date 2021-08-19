from typing import NamedTuple
from typing import Optional
from typing import List
from typing import Dict
from github import Github
from github import Repository
from github.GithubException import UnknownObjectException
import json
import datetime as dt
from bs4 import BeautifulSoup as Soup
# local modules
from all_repos_add_readme.github_utils.exceptions import RepoReadmeNeedsUpdate
from all_repos_add_readme.github_utils.constants import TOOL_NAME
from all_repos_add_readme.github_utils.constants import TOOL_COMMIT_MESSAGE
from all_repos_add_readme.github_utils.constants import TOOL_DISCLAIMER_MD


class GithubConfig(NamedTuple):
    username: str
    apiKey: str


class Repo:
    def __init__(self, repo: Repository.Repository) -> None:
        self._repo = repo
        self.tool_name = TOOL_NAME
        self.current_date = dt.date.today().strftime("%d/%m/%Y")
        # extracted properties
        self.full_name = repo.full_name
        self.description = repo.description if repo.description else ''
        self.created_at = repo.created_at
        self.updated_at = repo.updated_at
        self.total_commits = repo.get_commits().totalCount
        self.total_contributors = repo.get_contributors().totalCount
        self._used_languages = [
            {
                "language": language,
                "percentage": round(
                    100*(
                        total_lines / sum(repo.get_languages().values())
                    )
                    , 2
                )
            } for language, total_lines in repo.get_languages().items()
        ]

    @property
    def used_languages(self) -> List[Dict[str, float]]:
        return sorted(self._used_languages, key=lambda dict_: dict_["percentage"], reverse=True)

    def _inject_used_languages(self, formatted_readme: str) -> Soup:
        soup_object = Soup(formatted_readme, features="html.parser")
        used_language_ul = soup_object.find(id="used_languages")
        for i, language in enumerate(self.used_languages):
            current_language_tag = soup_object.new_tag("li")
            current_language_tag.string = f"{language['language']}: {str(language['percentage'])}%"
            used_language_ul.insert(position=i, new_child=current_language_tag)

        return soup_object

    def _append_tool_disclaimer(self, markdown_string: str) -> str:
        return markdown_string + "\n" + TOOL_DISCLAIMER_MD.format(**self.__dict__)

    def generate_readme_string(self, user_input: Optional[str]) -> str:
        if user_input:
            if isinstance(user_input, str):
                markdown_string = user_input
            else:
                raise NotImplementedError()

        else:
            with open("all_repos_add_readme/readme_template.md", 'r', encoding='utf-8') as readme_template_file:
                formatted_readme = readme_template_file.read().format(
                    **self.__dict__
                )

            with_formatted_languages = self._inject_used_languages(formatted_readme)
            markdown_string = with_formatted_languages.prettify().replace("&gt;", ">").replace("&lt:", "<")

        return self._append_tool_disclaimer(markdown_string)


def main(user_input: Optional[str]) -> None:
    with open('config.json', encoding='utf8') as config_file:
        github_config = GithubConfig(**json.load(config_file))

    github = Github(login_or_token=github_config.apiKey)
    for github_repo in set(github.get_user().get_repos(affiliation='owner')):
        if not github_repo.fork:
            try:
                readme_file = github_repo.get_contents(
                    github_repo.get_readme().path
                )
                readme_content = readme_file.decoded_content.decode()

                if TOOL_NAME in readme_content:
                    # repo already has a README.md file generate by the tool
                    # let's update its stats
                    raise RepoReadmeNeedsUpdate(readme_sha=readme_file.sha)

                else:
                    pass  # noop

            except UnknownObjectException as exc:  # no README
                if github_repo.name == "github-linter-CI":
                    print(f"creating README.md for {github_repo.name}")
                    _repo = Repo(repo=github_repo)
                    content = _repo.generate_readme_string(user_input)
                    if isinstance(exc, RepoReadmeNeedsUpdate):
                        github_repo.update_file(
                            path="README.md",
                            message=TOOL_COMMIT_MESSAGE,
                            content=content,
                            sha=exc.sha
                        )

                    else:
                        github_repo.create_file(
                            path="README.md",
                            message=TOOL_COMMIT_MESSAGE,
                            content=content,
                        )


if __name__ == "__main__":
    # some random input for testing purposes
    main(None)
