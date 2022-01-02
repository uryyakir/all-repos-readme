import argparse
from argparse import Namespace
from typing import Optional
from typing import Sequence
import os
import logging
# local modules
from all_repos_add_readme.github_utils import github_api
from all_repos_add_readme._exceptions import InvalidReadme, ExceptionMessages
from all_repos_add_readme.constants import Constants
from all_repos_add_readme.constants import LoggerConstants
from all_repos_add_readme.constants import ToolArgumentNames
from all_repos_add_readme._logger import setup_logger
from all_repos_add_readme._logger import shutdown_logging


logger = logging.getLogger(LoggerConstants.TOOL_LOGGER_NAME)


def _validate_markdown_input(res: Namespace) -> Optional[str]:
    # TODO: the best markdown-linter I found was a ruby one (https://github.com/markdownlint/markdownlint).
    #  To properly integrate it, I should either set up an API or install a ruby interpreter on the user's PC...
    #  Another option would be to instantiate the linter via GitHub actions (https://github.com/actionshub/markdownlint)
    if all([res.readme_file, res.readme_string]):
        raise InvalidReadme(message=ExceptionMessages.BOTH_STDIN_AND_FILE.value)

    elif res.readme_file:
        with open(os.path.join(os.getcwd(), res.readme_file)) as readme_file:
            logger.debug('found readme-file in provided path')
            return readme_file.read()

    elif res.readme_string:
        logger.debug('user provided a custom markdown string, using that')
        return res.readme_string

    logger.debug('readme-file and readme-string params are both not provided, resort to generating automated README.md file using template')
    return None


def unpack_arguments(res: Namespace) -> Namespace:
    for arg_name, arg_value in res.__dict__.items():
        if isinstance(arg_value, list) and len(arg_value) == 1:
            res.__setattr__(arg_name, arg_value[0])

    return res


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=Constants.TOOL_CLI_DESCRIPTION)
    parser.add_argument(*ToolArgumentNames.gen_argument_name(ToolArgumentNames.README_FILE_ARGUMENT, how='both'), nargs=1, help='path to readme file that would be added to all repos')
    parser.add_argument(*ToolArgumentNames.gen_argument_name(ToolArgumentNames.README_STRING_ARGUMENT, how='both'), nargs=1, help='markdown-supported string to be added as a README to all repos')
    parser.add_argument(*ToolArgumentNames.gen_argument_name(ToolArgumentNames.VERBOSE_ARGUMENT, how='both'), action='store_true', help='provide debugging information when running tool')
    parser.add_argument(*ToolArgumentNames.gen_argument_name(ToolArgumentNames.DRY_RUN_ARGUMENT, how='only full'), action='store_true', help='prevents tool from actually making commits to user\'s repo, but preforms the same workflow')
    parser.add_argument(*ToolArgumentNames.gen_argument_name(ToolArgumentNames.COMMIT_MESSAGE_ARGUMENT, how='only full'), nargs=1, help=f'provide a custom commit message for the creation or update of the README.md file.\nDefault: "{Constants.TOOL_COMMIT_MESSAGE}"')
    parser.add_argument(*ToolArgumentNames.gen_argument_name(ToolArgumentNames.LOG_TO_FILE_ARGUMENT, how='only full'), nargs='?', help='output tool logs to file', const=LoggerConstants().tool_default_logfile_name)
    parser.add_argument(*ToolArgumentNames.gen_argument_name(ToolArgumentNames.CONFIG_FILEPATH_ARGUMENT, how='only full'), nargs=1, help='path to config.json file that includes GitHub\'s api key')
    parser.add_argument(*ToolArgumentNames.gen_argument_name(ToolArgumentNames.REPOIGNORE_FILEPATH_ARGUMENT, how='only full'), nargs=1, help='path to .repoignore file')
    res = parser.parse_args(argv)

    res = unpack_arguments(res)
    input_ = _validate_markdown_input(res)
    setup_logger(logger_name=LoggerConstants.TOOL_LOGGER_NAME, verbose=res.verbose, log_file_name=res.log_to_file)
    github_api.main(input_, res.dry_run, res.commit_message, res.config_filepath, res.repoignore_filepath)

    shutdown_logging()

    return 0


if __name__ == '__main__':
    pass
    # exit(main(['-rs', """
    # # some string
    # ## some other string
    # <ul>
    #     <li>item1</li>
    #     <li>item12</li>
    # </ul>
    # """, "--dry-run"]))

    # exit(main(["--dry-run", "-v"]))

    # exit(main(['--readme-file', 'generic.md']))
