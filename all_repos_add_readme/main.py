import argparse
from argparse import Namespace
from typing import Optional
from typing import Sequence
from typing import TextIO
from typing import Union
import os
# local modules
from all_repos_add_readme.github_utils import github_api
from all_repos_add_readme.github_utils.exceptions import InvalidReadme, ExceptionMessages


def _validate_input(res: Namespace) -> Optional[str]:
    # TODO: the best markdown-linter I found was a ruby one (https://github.com/markdownlint/markdownlint).
    #  To properly integrate it, I should either set up an API or install a ruby interpreter on the user's PC...
    #  Another option would be to instantiate the linter via GitHub actions (https://github.com/actionshub/markdownlint)
    if all(res.__dict__.values()):
        raise InvalidReadme(message=ExceptionMessages.BOTH_STDIN_AND_FILE.value)

    elif not any(res.__dict__.values()):
        return None

    elif res.readme_file:
        with open(os.path.join(os.getcwd(), res.readme_file[0])) as readme_file:
            return readme_file.read()

    elif res.readme_string:
        return res.readme_string

    else:
        raise NotImplementedError("invalid user input!")


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        description="A tool to create a generic README.md for all of the user's owned REPOs.\n"
        "One can either provide a local readme-file (-rf) or provide a MD-formatted string (-rs).\n"
        "The provided input will be added to all of the user's owned REPOs that don't already have a readme file.\n"
        "If no input is provided, the tool will generate an automated README file for all REPOs.\n"
        "You can find the README default template under all_repos_add_readme/readme_template.md"
    )
    parser.add_argument('--readme-file', '-rf', nargs=1, help='path to readme file that should be added to all repos')
    parser.add_argument('--readme-string', '-rs', nargs=1, help='markdown-supported string to be added as a README to all repos')
    res = parser.parse_args(argv)
    input_ = _validate_input(res)
    github_api.main(input_)
    return 0


if __name__ == "__main__":
    # exit(main(['-rs', 'some string']))
    exit(main(['--readme-file', 'all_repos_add_readme/readme_template.md']))
