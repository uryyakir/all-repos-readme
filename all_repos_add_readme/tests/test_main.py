import pytest
from typing import Any
from typing import Dict
import os
# local modules
from conftest import TestConstants
from all_repos_add_readme.main import main
from all_repos_add_readme._exceptions import InvalidReadme
from all_repos_add_readme.constants import ToolArgumentNames


@pytest.mark.parametrize(
    'kwargs',
    (
        {
            'argv': [
                *ToolArgumentNames.gen_argument_name(ToolArgumentNames.README_STRING_ARGUMENT, how='only abbrev'),
                TestConstants.CUSTOM_README_STRING,
            ],
        },
        {
            'argv': [
                *ToolArgumentNames.gen_argument_name(ToolArgumentNames.README_STRING_ARGUMENT, how='only full'),
                TestConstants.CUSTOM_README_STRING,
            ],
        },
        {
            'argv': [
                *ToolArgumentNames.gen_argument_name(ToolArgumentNames.README_FILE_ARGUMENT, how='only full'),
                TestConstants.TEST_MARKDOWN_FILE_PATH,
            ],
        },
        {
            'argv': [
                *ToolArgumentNames.gen_argument_name(ToolArgumentNames.VERBOSE_ARGUMENT, how='only full'),
            ],
        },
        {
            'argv': [
                *ToolArgumentNames.gen_argument_name(ToolArgumentNames.VERBOSE_ARGUMENT, how='only full'),
            ],
        },
        {
            'argv': [
                *ToolArgumentNames.gen_argument_name(ToolArgumentNames.README_STRING_ARGUMENT, how='only full'),
                TestConstants.CUSTOM_README_STRING,
                *ToolArgumentNames.gen_argument_name(ToolArgumentNames.VERBOSE_ARGUMENT, how='only abbrev'),
            ],
        },
        {
            'argv': [
                *ToolArgumentNames.gen_argument_name(ToolArgumentNames.README_STRING_ARGUMENT, how='only full'),
                TestConstants.CUSTOM_README_STRING,
                *ToolArgumentNames.gen_argument_name(ToolArgumentNames.COMMIT_MESSAGE_ARGUMENT, how='only full'),
                TestConstants.TEST_CUSTOM_COMMIT_MESSAGE,
            ],
        },
        {
            'argv': [
                *ToolArgumentNames.gen_argument_name(ToolArgumentNames.LOG_TO_FILE_ARGUMENT, how='only full'),
            ],
        },
        {
            'argv': [
                *ToolArgumentNames.gen_argument_name(ToolArgumentNames.LOG_TO_FILE_ARGUMENT, how='only full'),
                TestConstants.CUSTOM_LOGFILE_NAME,
            ],
        },
        {
            'argv': [
                *ToolArgumentNames.gen_argument_name(ToolArgumentNames.README_FILE_ARGUMENT, how='only full'),
                TestConstants.TEST_MARKDOWN_FILE_PATH,
                *ToolArgumentNames.gen_argument_name(ToolArgumentNames.LOG_TO_FILE_ARGUMENT, how='only full'),
                TestConstants.CUSTOM_LOGFILE_NAME,
                *ToolArgumentNames.gen_argument_name(ToolArgumentNames.COMMIT_MESSAGE_ARGUMENT, how='only full'),
                TestConstants.TEST_CUSTOM_COMMIT_MESSAGE,
            ],
        },
        {
            'argv': [
                *ToolArgumentNames.gen_argument_name(ToolArgumentNames.README_FILE_ARGUMENT, how='only full'),
                TestConstants.TEST_MARKDOWN_FILE_PATH,
                *ToolArgumentNames.gen_argument_name(ToolArgumentNames.LOG_TO_FILE_ARGUMENT, how='only full'),
                TestConstants.CUSTOM_LOGFILE_NAME,
                *ToolArgumentNames.gen_argument_name(ToolArgumentNames.COMMIT_MESSAGE_ARGUMENT, how='only full'),
                TestConstants.TEST_CUSTOM_COMMIT_MESSAGE,
                *ToolArgumentNames.gen_argument_name(ToolArgumentNames.VERBOSE_ARGUMENT, how='only abbrev'),
            ],
        },
        {
            'argv': [
                *ToolArgumentNames.gen_argument_name(ToolArgumentNames.README_FILE_ARGUMENT, how='only full'),
                TestConstants.TEST_MARKDOWN_FILE_PATH,
                *ToolArgumentNames.gen_argument_name(ToolArgumentNames.LOG_TO_FILE_ARGUMENT, how='only full'),
                TestConstants.CUSTOM_LOGFILE_NAME,
                *ToolArgumentNames.gen_argument_name(ToolArgumentNames.COMMIT_MESSAGE_ARGUMENT, how='only full'),
                TestConstants.TEST_CUSTOM_COMMIT_MESSAGE,
                *ToolArgumentNames.gen_argument_name(ToolArgumentNames.VERBOSE_ARGUMENT, how='only abbrev'),
            ],
        },
        {
            'argv': [
                *ToolArgumentNames.gen_argument_name(ToolArgumentNames.README_FILE_ARGUMENT, how='only full'),
                os.path.join('..', TestConstants.TEST_MARKDOWN_FILE_PATH),
                *ToolArgumentNames.gen_argument_name(ToolArgumentNames.LOG_TO_FILE_ARGUMENT, how='only full'),
                TestConstants.CUSTOM_LOGFILE_NAME,
                *ToolArgumentNames.gen_argument_name(ToolArgumentNames.COMMIT_MESSAGE_ARGUMENT, how='only full'),
                TestConstants.TEST_CUSTOM_COMMIT_MESSAGE,
                *ToolArgumentNames.gen_argument_name(ToolArgumentNames.VERBOSE_ARGUMENT, how='only abbrev'),
                *ToolArgumentNames.gen_argument_name(ToolArgumentNames.CONFIG_FILEPATH_ARGUMENT, how='only full'),
                '../config.json',
                *ToolArgumentNames.gen_argument_name(ToolArgumentNames.REPOIGNORE_FILEPATH_ARGUMENT, how='only full'),
                '../.repoignore',
            ],
            'cd_dir': 'all_repos_add_readme/',
        },
    ),
)
def test_supported_cli_args(kwargs: Dict[str, Any]) -> None:
    # argv: List[str], cd_dir: os.PathLike = None
    argv = kwargs['argv']
    cd_dir = kwargs.get('cd_dir', None)

    _curr_path = os.path.abspath(os.getcwd())
    if cd_dir:
        os.chdir(cd_dir)

    _dry_run_arg = ToolArgumentNames.gen_argument_name(ToolArgumentNames.DRY_RUN_ARGUMENT, how='only full')[0]
    if _dry_run_arg not in argv:
        argv.append(_dry_run_arg)

    assert main(argv) == 0
    os.chdir(_curr_path)


def test_both_options_provided_exception() -> None:
    with pytest.raises(InvalidReadme):
        main([
            *ToolArgumentNames.gen_argument_name(ToolArgumentNames.README_STRING_ARGUMENT, how='only full'),
            TestConstants.CUSTOM_README_STRING,
            *ToolArgumentNames.gen_argument_name(ToolArgumentNames.README_FILE_ARGUMENT, how='only full'),
            TestConstants.TEST_MARKDOWN_FILE_PATH,
            *ToolArgumentNames.gen_argument_name(ToolArgumentNames.DRY_RUN_ARGUMENT, how='only full'),
        ])
