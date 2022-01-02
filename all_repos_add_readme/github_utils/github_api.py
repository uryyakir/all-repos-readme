from typing import Optional
from typing import Any
from typing import Dict
from github import Github
from github.Repository import Repository
from github.ContentFile import ContentFile
from github.GithubException import UnknownObjectException
import json
import sys
import logging
# local modules
from all_repos_add_readme._exceptions import RepoReadmeNeedsUpdate
from all_repos_add_readme.constants import LoggerConstants
from all_repos_add_readme.constants import LoggerColoring
from all_repos_add_readme.constants import GithubConstants
from all_repos_add_readme.constants import ToolArgumentNames
from all_repos_add_readme.constants import Constants
from all_repos_add_readme.github_utils._repo_ignore import RepoIgnore
from all_repos_add_readme.github_utils._github_repo import _Repo
from all_repos_add_readme.github_utils._github_config import _GithubConfig


logger = logging.getLogger(LoggerConstants.TOOL_LOGGER_NAME)


class GitHubAPI:
    def __init__(self, **kwargs: Any) -> None:
        self._user_input = kwargs[ToolArgumentNames.USER_INPUT_ARGUMENT]
        self._dry_run = kwargs[ToolArgumentNames.DRY_RUN_ARGUMENT]
        self._commit_message = (
            kwargs[ToolArgumentNames.COMMIT_MESSAGE_ARGUMENT] + Constants.TOOL_COMMIT_SIGNATURE
            if kwargs[ToolArgumentNames.COMMIT_MESSAGE_ARGUMENT]
            else Constants.TOOL_COMMIT_MESSAGE
        )
        self._repo_ignore = RepoIgnore(**kwargs)

    def run_tool(self, github_repo: Repository) -> Optional[Dict[str, str]]:
        _should_ignore = self._repo_ignore.should_ignore(github_repo)
        if not github_repo.fork and not _should_ignore:
            try:
                readme_file = github_repo.get_contents(
                    github_repo.get_readme().path,
                )
                assert isinstance(readme_file, ContentFile)
                readme_content = readme_file.decoded_content.decode()

                if Constants.TOOL_NAME in readme_content:
                    # repo already has a README.md file generate by the tool
                    # let's update its stats
                    logger.debug(f'found tool signature in {github_repo.full_name} README file - invoking README update')
                    raise RepoReadmeNeedsUpdate(readme_sha=readme_file.sha)

                else:
                    logger.debug(f'found a README in {github_repo.full_name} that does not contain tool signature - skipping')
                    return None  # noop

            except UnknownObjectException as exc:  # no README
                return self._run_tool(github_repo=github_repo, exception=exc)

        elif _should_ignore:
            logger.info(f'skipping {github_repo.full_name}: found in .repoignore')

        elif github_repo.fork:
            logger.debug(f"skipping {github_repo.full_name}: it's a fork")

        return None

    def _run_tool(self, github_repo: Repository, exception: UnknownObjectException) -> Optional[Dict[str, str]]:
        logger.info(f'creating README.md for {github_repo.full_name}')
        _repo = _Repo(repo=github_repo)
        readme_content = _repo.generate_readme_string(self._user_input)
        logger.debug(f'finished generating README.md content for repo {github_repo.full_name}')
        dry_run_indented_content = '\n'.join(['\t\t' + line for line in readme_content.split('\n')])
        if isinstance(exception, RepoReadmeNeedsUpdate):
            # specific UC where repo already has a README file generated by this tool
            # we would like to update the README's stats
            if not self._dry_run:
                response = github_repo.update_file(
                    path='README.md',
                    message=self._commit_message,
                    content=readme_content,
                    sha=exception.sha,
                )
                logger.debug(f'finished updating README.md file in repo {github_repo.full_name}!')
                return {github_repo.full_name: response['commit'].sha}

            else:
                logger.debug(
                    f'--- dry run: updating existing README.md in repo {github_repo.full_name}:\n'
                    f'\tCommit message: {self._commit_message}\n'
                    f'\tNew file content:\n{dry_run_indented_content}\n',
                )
                logger.info(f'--- dry run: updating existing README.md in repo {github_repo.full_name}')
                return None

        else:
            # first use UC, repo has no README so we need to generate one
            if not self._dry_run:
                response = github_repo.create_file(
                    path='README.md',
                    message=self._commit_message,
                    content=readme_content,
                )
                logger.debug(f'finished creating README.md file in repo {github_repo.full_name}!')
                return {github_repo.full_name: response['commit'].sha}

            else:
                logger.debug(
                    f'--- dry run: creating README.md in repo {github_repo.full_name}:\n'
                    f'\tCommit message: {self._commit_message}\n'
                    f'\tNew file content:\n{dry_run_indented_content}\n',
                )
                logger.info(f'--- dry run: creating README.md in repo {github_repo.full_name}')
                return None


def _get_config_json(config_filepath: Optional[str]) -> Dict[str, str]:
    with open(
            config_filepath if config_filepath else GithubConstants.GITHUB_CONFIG_FILE.value,
            encoding='utf8',
    ) as config_file:
        return json.load(config_file)


def main(
        user_input: Optional[str],
        dry_run: bool,
        commit_message: Optional[str] = None,
        config_filepath: Optional[str] = None,
        repoignore_filepath: Optional[str] = None,
        **kwargs: Any,
) -> int:
    changes_dict = {}
    github_api = GitHubAPI(**{**locals(), **kwargs})
    _config_content = _get_config_json(config_filepath=config_filepath)

    assert GithubConstants.API_KEY.value in _config_content.keys()
    github_config = _GithubConfig(**_config_content)

    github = Github(login_or_token=github_config.apiKey)
    for github_repo in set(github.get_user().get_repos(affiliation='owner')):
        did_action = github_api.run_tool(github_repo=github_repo)
        if did_action:
            changes_dict.update(did_action)

        logger.info(f"tool run on repo {github_repo.full_name}: {LoggerColoring.GREEN.value}done\n{LoggerColoring.RESET_SEQ.value}{'*' * 10}")

    if Constants.IS_TEST_RUN:
        print(json.dumps(changes_dict), file=sys.stderr)  # for testing purposes
    return 0
