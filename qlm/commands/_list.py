"""Command to list files in a remote repo."""

from typing import List, Optional, cast

from httpx import Response
from rich import print
from rich.panel import Panel
from typer import Argument, Exit, Option

from qlm.github.integrations import get_files_in_github_repo
from qlm.tools.config_helpers import get_config, is_offline
from qlm.tools.files import filter_for_markdown_files_only
from qlm.validators.github import validate_github_pat_token


def ls(
    directory: Optional[str] = Argument(
        "",
        help="The directory you want to list the contents of. Defaults to "
        "the repo root if omitted.",
    ),
    non_markdown: bool = Option(
        False, "--non-markdown", "-nm", help="Also list files that aren't markdown"
    ),
) -> None:
    """
    Lists markdown files in your remote. Online only :cry:

    To switch into online mode, run [bold cyan]qlm connect.
    """
    if is_offline():
        print(
            Panel(
                "[bold red1]You aren't connected to a remote. This command is for listing files in a remote. "
                "Use [cyan]ls[/cyan] or [cyan]dir[/cyan] for working with local files."
            )
        )
    else:
        remote: str = cast(str, get_config(key="remote_repo"))
        github_token: str = validate_github_pat_token()
        if not directory:
            directory = ""
        response: Response = get_files_in_github_repo(
            github_token=github_token, remote=remote, directory_path=directory
        )
        if not isinstance(response.json(), list):
            print(
                Panel(
                    f"[bold red1]The argument [cyan]{directory}[/cyan] is a file, not a directory"
                )
            )
            raise Exit()
        file_list: List[str] = [x["name"] for x in response.json()]
        filtered: List[str] = filter_for_markdown_files_only(file_list)
        directories: List[str] = [
            f"{x['name']}/" for x in response.json() if x["type"] == "dir"
        ]
        if non_markdown:
            print(file_list + directories)
        else:
            print(filtered + directories)
