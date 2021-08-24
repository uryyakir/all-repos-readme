import pytest
from typing import List
# local modules
from conftest import Constants
from all_repos_add_readme.main import main
from all_repos_add_readme._exceptions import InvalidReadme
from all_repos_add_readme.constants import ToolArgumentNames


@pytest.mark.parametrize(
    'argv',
    (
        [
            *ToolArgumentNames.gen_argument_name(ToolArgumentNames.README_STRING_ARGUMENT, how='only abbrev'),
            Constants.CUSTOM_README_STRING
        ],
        [
            *ToolArgumentNames.gen_argument_name(ToolArgumentNames.README_STRING_ARGUMENT, how='only full'),
            Constants.CUSTOM_README_STRING
        ],
        [
            *ToolArgumentNames.gen_argument_name(ToolArgumentNames.README_FILE_ARGUMENT, how='only full'),
            Constants.TEST_MARKDOWN_FILE_PATH
        ],
        [
            *ToolArgumentNames.gen_argument_name(ToolArgumentNames.VERBOSE_ARGUMENT, how='only full')
        ],
        [
            *ToolArgumentNames.gen_argument_name(ToolArgumentNames.VERBOSE_ARGUMENT, how='only full')
        ],
        [
            *ToolArgumentNames.gen_argument_name(ToolArgumentNames.README_STRING_ARGUMENT, how='only full'),
            Constants.CUSTOM_README_STRING,
            *ToolArgumentNames.gen_argument_name(ToolArgumentNames.VERBOSE_ARGUMENT, how='only abbrev')
        ],
        [
            *ToolArgumentNames.gen_argument_name(ToolArgumentNames.README_STRING_ARGUMENT, how='only full'),
            Constants.CUSTOM_README_STRING,
            *ToolArgumentNames.gen_argument_name(ToolArgumentNames.COMMIT_MESSAGE_ARGUMENT, how='only full'),
            Constants.TEST_CUSTOM_COMMIT_MESSAGE
        ],
        [
            *ToolArgumentNames.gen_argument_name(ToolArgumentNames.LOG_TO_FILE_ARGUMENT, how='only full')
        ],
        [
            *ToolArgumentNames.gen_argument_name(ToolArgumentNames.LOG_TO_FILE_ARGUMENT, how='only full'),
            Constants.CUSTOM_LOGFILE_NAME
        ],
        [
            *ToolArgumentNames.gen_argument_name(ToolArgumentNames.README_FILE_ARGUMENT, how='only full'),
            Constants.TEST_MARKDOWN_FILE_PATH,
            *ToolArgumentNames.gen_argument_name(ToolArgumentNames.LOG_TO_FILE_ARGUMENT, how='only full'),
            Constants.CUSTOM_LOGFILE_NAME,
            *ToolArgumentNames.gen_argument_name(ToolArgumentNames.COMMIT_MESSAGE_ARGUMENT, how='only full'),
            Constants.TEST_CUSTOM_COMMIT_MESSAGE
        ],
        [
            *ToolArgumentNames.gen_argument_name(ToolArgumentNames.README_FILE_ARGUMENT, how='only full'),
            Constants.TEST_MARKDOWN_FILE_PATH,
            *ToolArgumentNames.gen_argument_name(ToolArgumentNames.LOG_TO_FILE_ARGUMENT, how='only full'),
            Constants.CUSTOM_LOGFILE_NAME,
            *ToolArgumentNames.gen_argument_name(ToolArgumentNames.COMMIT_MESSAGE_ARGUMENT, how='only full'),
            Constants.TEST_CUSTOM_COMMIT_MESSAGE,
            *ToolArgumentNames.gen_argument_name(ToolArgumentNames.VERBOSE_ARGUMENT, how='only abbrev')
        ]
    )
)
def test_supported_cli_args(argv: List[str]) -> None:
    _dry_run_arg = ToolArgumentNames.gen_argument_name(ToolArgumentNames.DRY_RUN_ARGUMENT, how='only full')[0]
    if _dry_run_arg not in argv:
        argv.append(_dry_run_arg)

    assert main(argv) == 0


def test_both_options_provided_exception() -> None:
    with pytest.raises(InvalidReadme):
        main([
            *ToolArgumentNames.gen_argument_name(ToolArgumentNames.README_STRING_ARGUMENT, how='only full'),
            Constants.CUSTOM_README_STRING,
            *ToolArgumentNames.gen_argument_name(ToolArgumentNames.README_FILE_ARGUMENT, how='only full'),
            Constants.TEST_MARKDOWN_FILE_PATH,
            *ToolArgumentNames.gen_argument_name(ToolArgumentNames.DRY_RUN_ARGUMENT, how='only full')
        ])
