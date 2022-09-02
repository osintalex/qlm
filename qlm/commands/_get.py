"""Command to get files from a remote."""

from base64 import b64decode
from os import getcwd, path
from typing import Dict, cast

from rich import print
from rich.panel import Panel
from typer import Argument, Exit, Option

from qlm.github.integrations import download_file
from qlm.tools.config_helpers import get_config, is_offline
from qlm.validators.files import validate_file_path_is_empty
from qlm.validators.github import validate_github_pat_token


def get(
    file: str = Argument(..., help="Path to the remote file you want to download"),
    rename: str = Option(
        "", "--rename", "-r", help="Rename the file you want to download"
    ),
    directory: str = Option(
        "",
        "--directory",
        "-d",
        help="The local directory to save the file to. If not specified, "
        "qlm will download the file to your current working "
        "directory.",
    ),
) -> None:
    """
    Download a file from your remote :down_arrow:
    """

    if is_offline():
        print(
            Panel(
                "[bold red1] This is an online only command :sob: Use [cyan]qlm connect[/cyan] to go online :thumbs_up:"
            )
        )
        raise Exit()

    github_token: str = validate_github_pat_token()
    remote: str = cast(str, get_config(key="remote_repo"))
    file_data: Dict[str, str] = download_file(
        github_token=github_token, file=file, remote=remote
    ).json()
    if directory and rename:
        filepath_to_write: str = path.join(directory, rename)
    elif not directory and rename:
        filepath_to_write = path.join(getcwd(), rename)
    elif directory and not rename:
        filepath_to_write = path.join(directory, file_data["name"])
    else:
        filepath_to_write = path.join(getcwd(), file_data["name"])
    validate_file_path_is_empty(filepath_to_write)
    file_contents: str = b64decode(file_data["content"]).decode()
    with open(filepath_to_write, "w", encoding="utf-8") as f:
        f.write(file_contents)
    print(Panel(f"[bold green]Success! You downloaded file [yellow]{file}"))
