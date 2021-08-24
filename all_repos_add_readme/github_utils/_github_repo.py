from typing import List
from typing import Dict
from typing import Optional
from github import Repository
import datetime as dt
from bs4 import BeautifulSoup as Soup
import logging
# local modules
from all_repos_add_readme.constants import TOOL_DISCLAIMER_MD
from all_repos_add_readme.constants import TOOL_NAME
from all_repos_add_readme.constants import LoggerConstants
from all_repos_add_readme.constants import TOOL_README_TEMPLATE_PATH


logger = logging.getLogger(LoggerConstants.TOOL_LOGGER_NAME)


class _Repo:
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
                    100 * (
                        total_lines / sum(repo.get_languages().values())
                    ), 2
                )
            } for language, total_lines in repo.get_languages().items()
        ]
        logger.debug("finished extracting repo attributes")

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
        logger.debug("generating readme string for repo...")
        if user_input:
            if isinstance(user_input, str):
                markdown_string = user_input
            else:
                raise NotImplementedError()

        else:
            with open(TOOL_README_TEMPLATE_PATH, 'r', encoding='utf-8') as readme_template_file:
                formatted_readme = readme_template_file.read().format(
                    **self.__dict__
                )

            with_formatted_languages = self._inject_used_languages(formatted_readme)
            markdown_string = with_formatted_languages.prettify().replace("&gt;", ">").replace("&lt:", "<")

        return self._append_tool_disclaimer(markdown_string)
