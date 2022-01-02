import logging
import os
from github import Repository
import re
import warnings
from typing import Tuple
from typing import Any
from typing import Optional

# local modules
from all_repos_add_readme.logger_constants import LoggerConstants
from all_repos_add_readme.constants import GithubConstants
from all_repos_add_readme._exceptions import ExceptionMessages


logger = logging.getLogger(LoggerConstants.TOOL_LOGGER_NAME)


class RepoIgnore:
    def __init__(
        self,
        repoignore_filepath: Optional[str] = None,
        *,
        _test_patterns_lst: Tuple[str, ...] = (),
        **_: Any,
    ) -> None:
        if _test_patterns_lst:
            # tuple of patterns given for testing purposes
            # overwrites .repoignore patterns
            self._ignore_patterns = _test_patterns_lst

        else:
            try:
                with open(
                    os.path.join(
                        os.getcwd(),
                        repoignore_filepath
                        if repoignore_filepath
                        else GithubConstants.REPOIGNORE_FILE.value,
                    ),
                    encoding='utf-8',
                ) as repoignore_file:
                    self._ignore_patterns = tuple(
                        pattern.strip() for pattern in repoignore_file.readlines()
                    )

            except FileNotFoundError:
                warnings.warn(ExceptionMessages.NO_REPOIGNORE_FILE_WARNING.value, UserWarning)
                self._ignore_patterns = tuple()

    def should_ignore(self, repo: Repository.Repository) -> bool:
        for pattern in self._ignore_patterns:
            if re.match(pattern.lower(), repo.full_name.lower()) or re.match(
                pattern.lower(), repo.name.lower(),
            ):
                logger.debug(
                    f'{repo.full_name} matched the following regular expression: {pattern.lower()} (that appears in .repoignore)',
                )
                return True

        return False
