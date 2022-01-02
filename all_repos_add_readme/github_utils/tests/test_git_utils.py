import pytest
from _pytest.outcomes import Failed
from configparser import NoSectionError

# local modules
from all_repos_add_readme.github_utils.git_utils import GitConfigHandler
from conftest import TestConstants


@pytest.mark.run(order=1)
def test_getitem_does_not_exist(
    constants: TestConstants, git_config_handler_object: GitConfigHandler
) -> None:
    with pytest.raises(NoSectionError):
        _ = git_config_handler_object[constants.TEST_PROPERTY_PATH]


@pytest.mark.run(order=2)
def test_delitem_does_not_exist(
    constants: TestConstants, git_config_handler_object: GitConfigHandler
) -> None:
    assert not git_config_handler_object.__delitem__(constants.TEST_SECTION_NAME)


@pytest.mark.run(order=3)
def test_setitem(
    constants: TestConstants, git_config_handler_object: GitConfigHandler
) -> None:
    git_config_handler_object[
        constants.TEST_PROPERTY_PATH
    ] = constants.TEST_PROPERTY_VALUE
    with pytest.raises(Failed):  # sheeesh
        test_getitem_does_not_exist(**locals())


@pytest.mark.run(order=4)
def test_delitem(
    constants: TestConstants, git_config_handler_object: GitConfigHandler
) -> None:
    assert git_config_handler_object.__delitem__(constants.TEST_SECTION_NAME)
    test_getitem_does_not_exist(constants, git_config_handler_object)
