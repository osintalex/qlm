from os import getcwd, path
from typing import Dict
from base64 import b64decode

from typer import Argument, Option, Exit
from rich import print
from rich.panel import Panel

from qlm.tools.config_helpers import is_offline, get_config
from qlm.validators.github import validate_github_pat_token
from qlm.validators.files import validate_file_path_is_empty
from qlm.github.integrations import download_file


def get(file: str = Argument(..., help="Path to the remote file you want to download"),
        rename: str = Option("", "--rename", "-r", help="Rename the file you want to download"),
        filepath: str = Option("", "--filepath", "-fp", help="The local path to save the file to. If not specified, "
                                                             "qlm will download the file to your current working "
                                                             "directory.")) -> None:
    """
    Download a file from your remote :down_arrow:
    """

    if is_offline():
        print(Panel("[bold red1] This is an online only command :sob: Use [cyan]qlm connect[/cyan] to go online :thumbs_up:"))
        raise Exit()

    github_token: str = validate_github_pat_token()
    file_data: Dict[str, str] = download_file(github_token=github_token, file=file,
                                              remote=get_config(key="remote_repo")).json()
    if filepath and rename:
        filepath_to_write: str = path.join(filepath, rename)
    elif not filepath and rename:
        filepath_to_write: str = path.join(getcwd(), rename)
    elif filepath and not rename:
        filepath_to_write: str = path.join(filepath, file_data["name"])
    else:
        filepath_to_write: str = path.join(getcwd(), file_data["name"])
    validate_file_path_is_empty(filepath_to_write)
    file_contents: str = b64decode(file_data["content"]).decode()
    with open(filepath_to_write, "w") as f:
        f.write(file_contents)
    print(Panel(f"[bold green]Success! You downloaded file [yellow]{file}"))
