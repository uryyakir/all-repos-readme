import logging
import os
from github import Repository
import re
# local modules
from all_repos_add_readme.constants import TOOL_LOGGER_NAME


logger = logging.getLogger(TOOL_LOGGER_NAME)


class RepoIgnore:
    def __init__(self, path: str = '.repoignore') -> None:
        with open(os.path.join(os.getcwd(), path), 'r', encoding='utf-8') as repoignore_file:
            self._ignore_patterns = [pattern.strip() for pattern in repoignore_file.readlines()]

    def should_ignore(self, repo: Repository.Repository) -> bool:
        for pattern in self._ignore_patterns:
            if re.match(pattern.lower(), repo.full_name.lower()) or re.match(pattern.lower(), repo.name.lower()):
                logger.debug(f"{repo.full_name} matched the following regular expression: {pattern.lower()} (that appears in .repoignore)")
                return True

        return False
