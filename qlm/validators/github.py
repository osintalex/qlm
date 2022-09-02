"""Validators for github API operations."""

import os
from typing import Optional

import typer
from rich import print
from rich.panel import Panel


def validate_github_pat_token() -> str:
    """Checks to see if a github PAT token is set.

    :raise: typer.Exit() to quite the program if not.
    :return: the token if set.
    """

    github_token: Optional[str] = os.environ.get("qlm_token")
    if not github_token:
        print(
            Panel(
                """[bold red1]You didn't set the [hot_pink]qlm_token[/hot_pink] environment variable :x:
You can set it with this command [bold cyan]export qlm_token='YOUR TOKEN'[/bold cyan] where
[bold cyan]YOUR TOKEN[/bold cyan] is a Github PAT token authorized to access the repository."""
            )
        )
        raise typer.Exit()
    return github_token
