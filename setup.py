import os
from setuptools import setup
from shutil import copyfile
from typing import List

# local modules
from all_repos_add_readme.constants import Constants


def copy_data_files() -> None:
    # this function allows adding data files from root directory to package
    # when package is pip installed, those files will be present in package's folder in site-packages
    for _data_file in Constants.DATA_FILES:
        copyfile(
            os.path.join(os.getcwd(), _data_file),
            os.path.join(os.path.join(os.getcwd(), "all_repos_add_readme"), _data_file),
        )


def generate_install_requires() -> List[str]:
    with open(os.path.join(os.getcwd(), "requirements-dev.txt")) as reqs_file:
        _install_requires = reqs_file.read().split("\n")

    return _install_requires


if __name__ == "__main__":
    copy_data_files()
    setup(
        install_requires=generate_install_requires(),
    )
