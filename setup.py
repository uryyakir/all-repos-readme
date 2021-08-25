from setuptools import setup

with open("requirements.txt", 'r') as reqs_file:
    _install_requires = reqs_file.read().split("\n")

setup(install_requires=_install_requires)
