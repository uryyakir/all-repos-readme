import os
from setuptools import setup
# local modules
from all_repos_add_readme.constants import PACKAGE_DIR

with open(os.path.join(PACKAGE_DIR, "requirements.txt"), 'r') as reqs_file:
    _install_requires = reqs_file.read().split("\n")

setup(install_requires=_install_requires)
