import os
import pytest

# local modules
from conftest import TestConstants
from all_repos_add_readme.github_utils._github_repo import _Repo
from all_repos_add_readme.constants import Constants


def test_used_languages_property(get_repo_object: _Repo) -> None:
    assert get_repo_object.used_languages == [
        {'language': 'Python', 'percentage': 69.03},
        {'language': 'JavaScript', 'percentage': 18.71},
        {'language': 'Shell', 'percentage': 12.26},
    ]


def test_readme_template_exists() -> None:
    assert os.path.isfile(Constants.TOOL_README_TEMPLATE_PATH)


def test_generate_readme_string(
    get_repo_object: _Repo, constants: TestConstants,
) -> None:
    _none_readme_string = get_repo_object.generate_readme_string(None)
    _string_input = get_repo_object.generate_readme_string(constants.TOOL_TEST_STRING)
    with open(constants.TEST_MARKDOWN_FILE_PATH, encoding='utf-8') as test_md_file:
        _md_file_string = test_md_file.read()

    _file_input = get_repo_object.generate_readme_string(_md_file_string)

    for version in (_none_readme_string, _string_input, _file_input):
        assert (
            Constants.TOOL_NAME in version
            and constants.TOOL_SIGNATURE_STRING in version
        )


def test_generate_readme_string_invalid_input(get_repo_object: _Repo) -> None:
    with pytest.raises(NotImplementedError):
        _ = get_repo_object.generate_readme_string(['a', 'b'])  # type: ignore
