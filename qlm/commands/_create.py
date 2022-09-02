"""Command to create a new github repository."""

from rich import print
from rich.panel import Panel
from typer import Argument, Exit, Option, prompt

from qlm.github.integrations import create_new_repo
from qlm.tools.config_helpers import set_config
from qlm.validators.config import must_be_allowed_by_github
from qlm.validators.github import validate_github_pat_token


def create(
    repo_name: str = Argument(..., help="The name of the new repo to create"),
    public: bool = Option(
        False, "--public", "-p", help="Make a public, not private repository"
    ),
    force: bool = Option(
        False, "--force", "-f", help="Don't prompt before creating a new repo"
    ),
) -> None:
    """
    Creates and connects to a new repository in github under your personal account. The repository is private by default
     because privacy matters :fist:
    """

    github_token: str = validate_github_pat_token()
    if not force:
        print(
            Panel(
                f"You are going to create a new [hot_pink]{'public' if public else 'private'}[hot_pink] repo "
                f"[cyan]{repo_name}[cyan]"
            )
        )
        answer: str = prompt("Do you wish to proceed? [y/n]")
        if answer != "y":
            raise Exit()
    try:
        must_be_allowed_by_github(repo_name)
    except ValueError:
        print(
            Panel(
                f"[bold red1]The remote name [bold hot_pink]{repo_name}[/bold hot_pink] is not allowed by github :cry:"
            )
        )
        raise Exit()
    repo_full_name: str = create_new_repo(
        repo_name=repo_name, public=public, github_token=github_token
    )
    print(
        f"[green]Success! Created a new {'public' if public else 'private'} repo {repo_full_name}"
    )
    set_config(key="offline", value=False)
    set_config(key="remote_repo", value=repo_full_name)
    print(
        Panel(
            f"[bold green]You are now in online mode and connected to github repository [hot_pink]{repo_full_name}"
        )
    )
