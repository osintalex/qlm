"""Command to print out a file nicely on the console."""

from base64 import b64decode
from os import path
from typing import cast

from httpx import Response
from rich import print
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from typer import Argument, Exit, Option

from qlm.github.integrations import download_file
from qlm.tools.config_helpers import get_config, is_offline
from qlm.validators.github import validate_github_pat_token

console = Console()


def show(
    file: str = Argument(..., help="The path to the file you want see."),
    no_markdown: bool = Option(
        False, "--no-markup", "-nm", help="Print a file out without rendering markdown."
    ),
) -> None:
    """
    Prints your file to the console. Looks much nicer if you use markdown :innocent:
    """

    if is_offline():
        local_repo: str = cast(str, get_config(key="local_repo"))
        path_to_local_file: str = path.join(local_repo, file)
        if not path.exists(path_to_local_file):
            print(
                Panel(f"[bold red1]The file [cyan]{file}[/cyan] does not exist :sob:")
            )
            raise Exit()
        with open(path_to_local_file, "r", encoding="utf-8") as f:
            file_contents: str = f.read()
    else:
        remote: str = cast(str, get_config(key="remote_repo"))
        github_token: str = validate_github_pat_token()
        response: Response = download_file(
            github_token=github_token, remote=remote, file=file
        )
        file_contents = b64decode(response.json()["content"]).decode()

    if no_markdown:
        print(file_contents)
    else:
        rendered_markdown: Markdown = Markdown(file_contents)
        console.print(rendered_markdown)
