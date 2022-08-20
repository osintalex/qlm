from typer import Argument
from rich import print
from rich.panel import Panel

from ..tools.config_helpers import set_config
from ..validators.github import validate_github_pat_token
from ..github.integrations import check_github_connection


def connect(remote: str = Argument(..., help="The name of the remote github repository where your notes are, "
                                              "e.g. [yellow]my-username/repo-name")) -> None:
    """
    Checks if you can connect to github and sets your config to online. You must set the environment variable [hot_pink]$qlm_token[/hot_pink] to connect.

    You must specify the full name of the repo in the format <username>/<repo>. If you don't, qlm will attempt to find the repo under your personal account username.
    """
    github_token: str = validate_github_pat_token()
    check_github_connection(github_token=github_token, remote=remote)
    set_config(key="offline", value=False)
    print(Panel(f"[bold green]Success! You are connected to github repository [bold hot_pink]{remote}[/bold hot_pink] :boom:"))
