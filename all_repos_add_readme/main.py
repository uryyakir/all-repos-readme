import argparse
from argparse import Namespace
from typing import Optional
from typing import Sequence
# local modules
from all_repos_add_readme.github_utils import github_api


def _validate_input(res: Namespace) -> None:
    # TODO: the best markdown-linter I found was a ruby one (https://github.com/markdownlint/markdownlint).
    #  To properly integrate it, I should either set up an API or install a ruby interpreter on the user's PC...
    #  Another option would be to instantiate the linter via GitHub actions (https://github.com/actionshub/markdownlint)
    pass


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="A tool to create a generic README.md for all_repos")
    parser.add_argument('--readme-file', '-rf', nargs=1, help='path to readme file that should be added to all repos')
    parser.add_argument('--readme-string', '-rs', nargs=1, help='markdown-supported string to be added as a README to all repos')
    res = parser.parse_args(argv)
    _validate_input(res)
    github_api.main(res)
    print(res)
    return 0


if __name__ == "__main__":
    exit(main(['-rs', 'some string']))
    # exit(main(['--readme-file value']))
