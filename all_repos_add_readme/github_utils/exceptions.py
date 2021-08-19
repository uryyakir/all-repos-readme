from enum import Enum
from github.GithubException import UnknownObjectException


class InvalidReadme(BaseException):
    def __init__(self, message: str) -> None:
        super(InvalidReadme, self).__init__(message)


class RepoReadmeNeedsCreationOrUpdate(UnknownObjectException):
    def __init__(self) -> None:
        super(RepoReadmeNeedsCreationOrUpdate, self).__init__("", "", {})


class ExceptionMessages(Enum):
    BOTH_STDIN_AND_FILE = "both a readme-string and a readme-file were provided. Please make sure you only provide one!"
    NONE_PROVIDED = "neither a readme-string nor a readme-file were provided. Please make sure you provide one!"
