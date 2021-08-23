import os
import sys
import json
import re
import pytest
from configparser import NoSectionError
# local modules
from all_repos_add_readme.github_utils.git_utils import GitConfigHandler
from all_repos_add_readme.constants import GithubConstants
from all_repos_add_readme.constants import GitConstants
# import hooks python code
sys.path.append(os.path.join(os.getcwd(), ".githooks/_post_commit"))
sys.path.append(os.path.join(os.getcwd(), ".githooks/_pre_commit"))
import _restore_creds  # noqa
import _censor_creds  # noqa


def test_hooks(git_config_handler_object: GitConfigHandler) -> None:
    with open(GithubConstants.GITHUB_CONFIG_FILE.value, 'r', encoding='utf-8') as config_file:
        config_json = json.load(config_file)
    # assert a private github api key currently exists in config.json
    private_api_key = config_json[GithubConstants.API_KEY.value]
    assert re.match(r"\w+", private_api_key)
    # censor github api key
    assert _censor_creds.main() == 1

    with open(GithubConstants.GITHUB_CONFIG_FILE.value, 'r', encoding='utf-8') as config_file:
        config_json = json.load(config_file)

    # assert the key is censored
    assert config_json[GithubConstants.API_KEY.value] == "..."
    # assert the key is stored in .git/config
    assert git_config_handler_object[GitConstants.API_KEY_CONFIG_PROPERTY.value] == private_api_key
    # assert invoking _censor_creds again does nothing (exit code 0)
    assert _censor_creds.main() == 0
    # restore github api key back into config.json
    assert _restore_creds.main() == 0
    with pytest.raises(NoSectionError):
        # assert section was deleted from .git/config
        _ = git_config_handler_object[GitConstants.API_KEY_CONFIG_PROPERTY.value]

    with open(GithubConstants.GITHUB_CONFIG_FILE.value, 'r', encoding='utf-8') as config_file:
        config_json = json.load(config_file)

    # assert private key is back in config.json
    assert config_json[GithubConstants.API_KEY.value] == private_api_key
