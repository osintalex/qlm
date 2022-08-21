from shutil import which
from re import fullmatch, compile, Pattern
from typing import List, Optional, Any, Dict
from os.path import exists

from rich import print
from rich.panel import Panel
from typer import Exit
from pydantic import BaseModel, ValidationError, validator

from qlm.tools.config_helpers import CONFIG_TYPE


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


class OfflineFilesModel(BaseModel):
    """Model for validating the list of offline files to add."""

    repo_filepath: str
    local_filepath: str
    remote: str

    _validate_remote_: classmethod = validator("remote", allow_reuse=True)(must_be_allowed_by_github)
    _validate_local_filepath: classmethod = validator("local_filepath", allow_reuse=True)(path_must_exist)


class ConfigModel(BaseModel):
    """Model to validate configuration data."""

    offline: bool
    text_editor: str
    local_repo: Optional[str] = None
    remote_repo: Optional[str] = None
    offline_files_to_add: Optional[List[OfflineFilesModel]] = None

    _validate_remote_: classmethod = validator("remote_repo", allow_reuse=True)(must_be_allowed_by_github)
    _validate_local_repo_: classmethod = validator("local_repo", allow_reuse=True)(path_must_exist)
    _validate_text_editor: classmethod = validator("text_editor", allow_reuse=True)(must_be_executable)

    @validator("offline")
    def must_be_boolean(cls, value: Any) -> bool:
        """Checks if a the offline value is correct.

        :param value: The value to check against.
        :raise: ValueError in case of the offline entry isn't true/false.
        :return: The offline entry if valid.
        """
        if value not in {True, False}:
            raise ValueError('Offline must be boolean')
        return value


def validate_new_config(user_config: Dict[str, Any]) -> CONFIG_TYPE:
    """Validate  user supplied configuration data.

    :param user_config: The user supplied configuration data.
    :raise: Exit in case of incorrect configurations.
    :return: The validated configuration data.
    """

    try:
        return ConfigModel(**user_config).dict(exclude_none=True)
    except ValidationError as error_message:
        print(Panel(f"[bold red1] There was an error validating your config: {error_message}"))
        raise Exit()
