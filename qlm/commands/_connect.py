from typer import Argument, Exit
from rich import print
from rich.panel import Panel

from qlm.tools.config_helpers import set_config
from qlm.validators.github import validate_github_pat_token
from qlm.validators.config import must_be_allowed_by_github
from qlm.github.integrations import check_github_connection


def connect(remote: str = Argument(..., help="The name of the remote github repository where your notes are, "
                                              "e.g. [yellow]my-username/repo-name")) -> None:
    """
    Checks if you can connect to github and sets your config to online. You must set the environment variable [hot_pink]$qlm_token[/hot_pink] to connect.

    You must specify the full name of the repo in the format <username>/<repo>. If you don't, qlm will attempt to find the repo under your personal account username.
    """

    try:
        must_be_allowed_by_github(remote)
    except ValueError:
        print(Panel(f"[bold red1]The remote name [bold hot_pink]{remote}[/bold hot_pink] is not allowed by github :cry:"))
        raise Exit()
    github_token: str = validate_github_pat_token()
    result: bool = check_github_connection(github_token=github_token, remote=remote)
    if result:
        set_config(key="offline", value=False)
        print(Panel(f"[bold green]Success! You are connected to github repository [bold hot_pink]{remote}[/bold hot_pink] :boom:"))
    else:
        print(Panel(f"[bold red1]Could not connect to github repository [bold hot_pink]{remote}[/bold hot_pink] :cry:"))
