import json
import os
import sys
# local modules
sys.path.insert(0, os.getcwd())
from all_repos_add_readme.constants import GithubConstants  # noqa


def main() -> int:
    with open(GithubConstants.GITHUB_CONFIG_FILE.value, encoding='utf-8') as config_file:
        config_json = json.load(config_file)

    config_json[GithubConstants.API_KEY.value] = os.environ['GITHUB_API_KEY']
    with open(GithubConstants.GITHUB_CONFIG_FILE.value, mode='w', encoding='utf-8') as out_config_file:
        json.dump(config_json, out_config_file, indent=2)

    return 0


if __name__ == '__main__':
    exit(main())
