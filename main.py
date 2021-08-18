import argparse
from typing import Optional
from typing import Sequence


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="A tool to create a generic README.md for all_repos")
    parser.add_argument('--readme-file', '-rf', nargs=1, help='path to readme file that should be added to all repos')
    parser.add_argument('--readme-string', '-rs', nargs=1, help='markdown-supported string to be added as a README to all repos')
    res = parser.parse_args(argv)
    print(res)


if __name__ == "__main__":
    exit(main(['-rs', 'some strnig']))
    # exit(main(['--readme-file value']))
