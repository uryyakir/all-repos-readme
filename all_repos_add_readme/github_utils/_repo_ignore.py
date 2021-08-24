import logging
import os
from github import Repository
import re
from typing import Tuple
from typing import Any
# local modules
from all_repos_add_readme.constants import LoggerConstants
from all_repos_add_readme.constants import PACKAGE_DIR


logger = logging.getLogger(LoggerConstants.TOOL_LOGGER_NAME)


class RepoIgnore:
    def __init__(self, path: str = os.path.join(PACKAGE_DIR, '.repoignore'), *, _test_patterns_lst: Tuple[str, ...] = (), **_: Any) -> None:
        if _test_patterns_lst:
            # tuple of patterns given for testing purposes
            # overwrites .repoignore patterns
            self._ignore_patterns = _test_patterns_lst

        else:
            with open(os.path.join(os.getcwd(), path), 'r', encoding='utf-8') as repoignore_file:
                self._ignore_patterns = tuple((pattern.strip() for pattern in repoignore_file.readlines()))

    def should_ignore(self, repo: Repository.Repository) -> bool:
        for pattern in self._ignore_patterns:
            if re.match(pattern.lower(), repo.full_name.lower()) or re.match(pattern.lower(), repo.name.lower()):
                logger.debug(f"{repo.full_name} matched the following regular expression: {pattern.lower()} (that appears in .repoignore)")
                return True

        return False
