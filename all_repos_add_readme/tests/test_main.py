import pytest
from typing import List
# local modules
from conftest import Constants
from all_repos_add_readme.main import main
from all_repos_add_readme._exceptions import InvalidReadme


@pytest.mark.parametrize(
    'argv',
    (
        ['-rs', Constants.CUSTOM_README_STRING],
        ['--readme-string', Constants.CUSTOM_README_STRING],
        ['--readme-file', Constants.TEST_MARKDOWN_FILE_PATH],
        ['--verbose'],
        ['-v'],
        ['--readme-string', Constants.CUSTOM_README_STRING, '-v'],
        ['--readme-string', Constants.CUSTOM_README_STRING, '--commit-message', Constants.TEST_CUSTOM_COMMIT_MESSAGE],
        ['--log-to-file'],
        ['--log-to-file', Constants.CUSTOM_LOGFILE_NAME],
        ['--readme-file', Constants.TEST_MARKDOWN_FILE_PATH, '--log-to-file', Constants.CUSTOM_LOGFILE_NAME, '--commit-message', Constants.TEST_CUSTOM_COMMIT_MESSAGE],
        ['--readme-file', Constants.TEST_MARKDOWN_FILE_PATH, '--log-to-file', Constants.CUSTOM_LOGFILE_NAME, '--commit-message', Constants.TEST_CUSTOM_COMMIT_MESSAGE, '-v']
    )
)
def test_supported_cli_args(argv: List[str]) -> None:
    if "--dry-run" not in argv:
        argv.append("--dry-run")

    assert main(argv) == 0


def test_both_options_provided_exception() -> None:
    with pytest.raises(InvalidReadme):
        main(["--readme-string", Constants.CUSTOM_README_STRING, "--readme-file", Constants.TEST_MARKDOWN_FILE_PATH, "--dry-run"])
