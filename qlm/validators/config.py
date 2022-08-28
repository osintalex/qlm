from shutil import which
from re import fullmatch, compile, Pattern
from typing import  Any
from os.path import exists


allowed_github_repo: Pattern = compile(r"[A-Za-z0-9_.\-/]+")


def validate_offline_flag(value: Any) -> bool:
    """Checks that the input for offline is a valid boolean.

    :param value: The value to check against.
    :raise ValueError in case of an invalid input.
    "return: The flag if valid.
    """

    clean: str = value.strip().lower()
    if clean not in {"false", "true"}:
        raise ValueError(f"The input {value} is not valid. Only True and False are allowed!")
    return {"false": False, "true": True}[clean]


def must_be_allowed_by_github(value: Any) -> str:
    """Checks if a remote is allowed by github.

    :param value: The value to check against.
    :raise: ValueError in case of an invalid remote.
    :return: The remote if valid.
    """
    if not fullmatch(allowed_github_repo, value):
        raise ValueError(f"The characters in remote {value} are not allowed by github")
    return value


def path_must_exist(value: Any) -> str:
    """Checks if a local directory path exists.

    :param value: The value to check against.
    :raise: ValueError in case of an invalid directory path.
    :return: The directory path if valid.
    """
    if not exists(value):
        raise ValueError(f"The local repo path {value} does not exist")
    return value


def must_be_executable(value: Any) -> str:
    """Checks if a text editor exists as an executable on the system.

    :param value: The value to check against.
    :raise: ValueError in case the text editor value doesn't exist.
    :return: The text editor executable if it exists.
    """
    if not which(value):
        raise ValueError(f"The value for text_editor {value} is not an executable")
    return value
