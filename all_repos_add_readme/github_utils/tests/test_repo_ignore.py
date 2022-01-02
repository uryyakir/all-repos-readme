import pytest
from github.Repository import Repository

# local modules
from conftest import TestConstants
from all_repos_add_readme.github_utils._repo_ignore import RepoIgnore


@pytest.mark.parametrize(
    ('expression', 'should_filter'),
    [
        (r'.*', True),
        (TestConstants.TEST_AGAINST_REPO_NAME, True),
        (r'\w+', True),
        (
            TestConstants.TEST_AGAINST_USERNAME
            + '/'
            + TestConstants.TEST_AGAINST_REPO_NAME,
            True,
        ),
        ('other_random_repo', False),
    ],
)
def test_repo_ignore(
    get_github_repository_object: Repository, expression: str, should_filter: bool,
) -> None:
    _repo_ignore = RepoIgnore(_test_patterns_lst=(expression,))
    assert _repo_ignore.should_ignore(get_github_repository_object) is should_filter


def test_missing_repoignore_file() -> None:
    with pytest.warns(UserWarning):
        _repo_ignore = RepoIgnore(repoignore_filepath="random/path/.repoignore")

    assert _repo_ignore._ignore_patterns == tuple()
