"""Command to edit files."""

import asyncio
import os
from base64 import b64decode
from tempfile import NamedTemporaryFile
from typing import cast

from httpx import Response
from rich import print
from rich.panel import Panel
from typer import Argument, Exit

from qlm.github.integrations import add_files_to_github, download_file
from qlm.tools.config_helpers import get_config, is_offline
from qlm.validators.github import validate_github_pat_token


def edit(
    file: str = Argument(
        ...,
        help="The path to the file you want to edit relative to remote or local repo root.",
    )
) -> None:
    """
    Edit a file :man_cartwheeling:

    Uses vim by default. You can change the text editor using [bold cyan]qlm config --editor.
    """

    if is_offline():
        local_repo: str = cast(str, get_config(key="local_repo"))
        path_to_file_for_editing: str = os.path.join(local_repo, file)
        if not os.path.exists(path_to_file_for_editing):
            print(
                Panel(
                    f"[bold red1] The file [yellow]{file}[/yellow] doesn't exist :confused:"
                )
            )
            raise Exit()
        if os.path.isdir(path_to_file_for_editing):
            print(f"Oh no, {file} is a directory not a file!")
            print(
                Panel(
                    f"[bold red1] The file [yellow]{file}[/yellow] is a directory not a file :confused:"
                )
            )
            raise Exit()

        os.system(f"{get_config(key='editor')} {path_to_file_for_editing}")
    else:
        github_token: str = validate_github_pat_token()
        remote: str = cast(str, get_config(key="remote_repo"))
        response: Response = download_file(
            github_token=github_token, remote=remote, file=file
        )
        with NamedTemporaryFile() as tmp:
            with open(tmp.name, "w", encoding="utf-8") as f:
                f.write(b64decode(response.json()["content"]).decode())
                f.seek(0)
        os.system(f"{get_config(key='editor')} {tmp.name}")
        asyncio.run(
            add_files_to_github(
                files_to_publish=[
                    {
                        "local_filepath": tmp.name,
                        "repo_filepath": file,
                        "remote": remote,
                    }
                ],
                github_token=github_token,
            )
        )
