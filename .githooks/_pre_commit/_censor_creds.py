import json
import re
from github_utils.github_constants import GithubConstants


def main() -> int:
    with open(GithubConstants.GITHUB_CONFIG_FILE.value, mode='r', encoding='utf-8') as config_file:
        config_json = json.load(config_file)
        if re.match(r"\w+", config_json[GithubConstants.API_KEY.value]):
            config_json[GithubConstants.API_KEY.value] = '...'
            with open(GithubConstants.GITHUB_CONFIG_FILE.value, mode='w', encoding='utf-8') as out_config_file:
                json.dump(config_json, out_config_file, indent=2)

            return 1

    return 0


if __name__ == "__main__":
    print("random change")
    exit(main())  # exit with an exit-code indicating whether a change was needed or not
