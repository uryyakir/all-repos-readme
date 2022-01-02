import json
from configparser import NoOptionError, NoSectionError

# local modules
from all_repos_add_readme.constants import GithubConstants
from all_repos_add_readme.github_utils.git_utils import GitConstants
from all_repos_add_readme.github_utils.git_utils import git_config


def main() -> int:
    with open(
        GithubConstants.GITHUB_CONFIG_FILE.value, encoding='utf-8',
    ) as config_file:
        config_json = json.load(config_file)
        try:
            api_key = git_config[GitConstants.API_KEY_CONFIG_PROPERTY.value]
            config_json[GithubConstants.API_KEY.value] = api_key
            with open(
                GithubConstants.GITHUB_CONFIG_FILE.value, mode='w', encoding='utf-8',
            ) as out_config_file:
                json.dump(config_json, out_config_file, indent=2)

            del git_config[GitConstants.API_KEY_CONFIG_SECTION.value]

        except (
            NoOptionError,
            NoSectionError,
        ):  # key was not set in pre-commit hook, probably because api_key was already censored
            pass

    return 0


if __name__ == '__main__':
    exit(main())
