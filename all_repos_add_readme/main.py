import argparse
from argparse import Namespace
from typing import Optional
from typing import Sequence
import os
# local modules
from all_repos_add_readme.github_utils import _github_api
from all_repos_add_readme._exceptions import InvalidReadme, ExceptionMessages
from all_repos_add_readme.constants import TOOL_CLI_DESCRIPTION


def _validate_input(res: Namespace) -> Optional[str]:
    # TODO: the best markdown-linter I found was a ruby one (https://github.com/markdownlint/markdownlint).
    #  To properly integrate it, I should either set up an API or install a ruby interpreter on the user's PC...
    #  Another option would be to instantiate the linter via GitHub actions (https://github.com/actionshub/markdownlint)
    if all([res.readme_file, res.readme_string]):
        raise InvalidReadme(message=ExceptionMessages.BOTH_STDIN_AND_FILE.value)

    elif not any([res.readme_file, res.readme_string]):
        return None

    elif res.readme_file:
        with open(os.path.join(os.getcwd(), res.readme_file[0])) as readme_file:
            return readme_file.read()

    elif res.readme_string:
        return res.readme_string[0]

    else:
        raise NotImplementedError("invalid user input!")


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=TOOL_CLI_DESCRIPTION)
    parser.add_argument('--readme-file', '-rf', nargs=1, help='path to readme file that should be added to all repos')
    parser.add_argument('--readme-string', '-rs', nargs=1, help='markdown-supported string to be added as a README to all repos')
    parser.add_argument('--dry-run', '-dr', action='store_true', help='prevents tool from actually making commits to user\'s repo, but preforms the same run-flow')
    res = parser.parse_args(argv)
    input_ = _validate_input(res)
    _github_api.main(input_, res.dry_run)
    return 0


if __name__ == "__main__":
    # exit(main(['-rs', """
    # # some string
    # ## some other string
    # <ul>
    #     <li>item1</li>
    #     <li>item12</li>
    # </ul>
    # """, "--dry-run"]))
    exit(main(["--dry-run"]))
    # exit(main(['--readme-file', 'generic.md']))
