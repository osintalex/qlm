"""Command to download a github remote to your local machine."""

import os
from tempfile import TemporaryDirectory
from typing import cast
from zipfile import ZipFile

from httpx import Response
from rich import print
from rich.panel import Panel
from typer import Argument, Exit, Option

from qlm.github.integrations import download_github_repository
from qlm.tools.config_helpers import get_config, is_offline
from qlm.validators.config import must_be_allowed_by_github
from qlm.validators.github import validate_github_pat_token


def download(
    local: str = Argument(
        ..., help="The absolute path to where you want to keep your notes"
    ),
    remote: str = Option(
        "",
        "--remote",
        "-r",
        help="The name of the remote you want to download files from. "
        "Defaults to whatever is in your config.",
    ),
) -> None:
    """
    Downloads your notes from a remote to a local repository. Online only command :cry:

    To switch into online mode, run [bold cyan]qlm connect.
    """

    if is_offline():
        print(
            Panel(
                """[bold red1]You are not in online mode :cry: Run [cyan]qlm connect[/cyan]
                to switch to online mode :wink:"""
            )
        )
        raise Exit()

    github_token: str = validate_github_pat_token()
    if remote:
        try:
            remote = must_be_allowed_by_github(remote)
        except ValueError:
            print(
                Panel(
                    f"[bold red_1]The characters in {remote} are not allowed by github :cry:"
                )
            )
            raise Exit()
    else:
        remote = cast(str, get_config(key="remote_repo"))

    response: Response = download_github_repository(
        github_token=github_token, remote=remote
    )
    with TemporaryDirectory() as temp_dir:
        zip_file_path: str = os.path.join(temp_dir, "repo.zip")
        with open(zip_file_path, "wb") as f:
            f.write(response.content)
        with ZipFile(zip_file_path, "r") as zip_f:
            archive_folder_name: str = zip_f.namelist()[0]
            zip_f.extractall(local)
    print(
        Panel(
            f"[bold green]Successfully downloaded repo to directory: [yellow]"
            f"{os.path.join(local, archive_folder_name)}"
        )
    )
