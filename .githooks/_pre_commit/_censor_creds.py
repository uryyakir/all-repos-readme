import json
import re

# local modules
from all_repos_add_readme.constants import GithubConstants
from all_repos_add_readme.github_utils.git_utils import GitConstants
from all_repos_add_readme.github_utils.git_utils import git_config


def main() -> int:
    with open(
        GithubConstants.GITHUB_CONFIG_FILE.value, encoding='utf-8',
    ) as config_file:
        config_json = json.load(config_file)
        curr_api_key = config_json[GithubConstants.API_KEY.value]
        if re.match(r'\w+', curr_api_key):
            # this git config custom variable will later be used to restore the apiKey and allow continuous development
            git_config[GitConstants.API_KEY_CONFIG_PROPERTY.value] = curr_api_key

            config_json[GithubConstants.API_KEY.value] = '...'
            with open(
                GithubConstants.GITHUB_CONFIG_FILE.value, mode='w', encoding='utf-8',
            ) as out_config_file:
                json.dump(config_json, out_config_file, indent=2)

            return 1

    return 0


if __name__ == '__main__':
    exit(main())  # exit with an exit-code indicating whether a change was needed or not
