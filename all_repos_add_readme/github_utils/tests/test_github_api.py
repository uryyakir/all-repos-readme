import json
from github.Repository import Repository
from _pytest.capture import CaptureFixture
from typing import Dict
# local modules
from conftest import Constants
from conftest import get_last_commit
from all_repos_add_readme.github_utils import github_api
from all_repos_add_readme.constants import TOOL_COMMIT_SIGNATURE


def _assert_expected_exit_code(capsys: CaptureFixture, exit_code: int, expected_err_json_len: int) -> Dict[str, str]:
    assert exit_code == 0

    _, err = capsys.readouterr()
    err_json = json.loads(err)
    assert len(err_json) == expected_err_json_len

    return err_json


def test_tool_run(capsys: CaptureFixture, get_github_repository_object: Repository, constants: Constants) -> None:
    exit_code = github_api.main(user_input=None, dry_run=False, _test_patterns_lst=constants.ONLY_TEST_AGAINST_REPO_FILTER)
    err_json = _assert_expected_exit_code(capsys, exit_code, 1)

    assert get_last_commit(get_github_repository_object).sha == err_json[get_github_repository_object.full_name]


def test_tool_dry_run(capsys: CaptureFixture, constants: Constants) -> None:
    exit_code = github_api.main(user_input=None, dry_run=True, _test_patterns_lst=constants.ONLY_TEST_AGAINST_REPO_FILTER)
    _ = _assert_expected_exit_code(capsys, exit_code, 0)


def test_tool_custom_commit_message(capsys: CaptureFixture, get_github_repository_object: Repository, constants: Constants) -> None:
    exit_code = github_api.main(user_input=None, dry_run=False, commit_message=[constants.TEST_CUSTOM_COMMIT_MESSAGE], _test_patterns_lst=constants.ONLY_TEST_AGAINST_REPO_FILTER)
    _ = _assert_expected_exit_code(capsys, exit_code, 1)

    assert get_last_commit(get_github_repository_object).commit.message.startswith(constants.TEST_CUSTOM_COMMIT_MESSAGE) and \
           get_last_commit(get_github_repository_object).commit.message.endswith(TOOL_COMMIT_SIGNATURE)


def test_tool_custom_user_input(capsys: CaptureFixture, get_github_repository_object: Repository, constants: Constants) -> None:
    exit_code = github_api.main(user_input=constants.TEST_USER_INPUT, dry_run=False, _test_patterns_lst=constants.ONLY_TEST_AGAINST_REPO_FILTER)
    _ = _assert_expected_exit_code(capsys, exit_code, 1)

    readme_file = get_github_repository_object.get_contents(
        get_github_repository_object.get_readme().path
    )
    readme_content = readme_file.decoded_content.decode()
    assert readme_content.startswith(constants.TEST_USER_INPUT) and \
           readme_content.endswith(constants.TOOL_SIGNATURE_STRING)
