import os
from setuptools import setup
from shutil import copyfile
from typing import List
# local modules
from all_repos_add_readme.constants import BASE_DIR
from all_repos_add_readme.constants import PACKAGE_DIR
from all_repos_add_readme.constants import DATA_FILES


def copy_data_files() -> None:
    # this function allows adding data files from root directory to package
    # when package is pip installed, those files will be present in package's folder in site-packages
    # currently, no such files are needed
    for _data_file in DATA_FILES:
        copyfile(os.path.join(BASE_DIR, _data_file), os.path.join(PACKAGE_DIR, _data_file))


def generate_install_requires() -> List[str]:
    with open(os.path.join(BASE_DIR, "requirements.txt"), 'r') as reqs_file:
        _install_requires = reqs_file.read().split("\n")

    return _install_requires


if __name__ == "__main__":
    copy_data_files()
    setup(
        install_requires=generate_install_requires(),
    )
