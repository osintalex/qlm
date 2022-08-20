import asyncio
from typing import List, Dict, cast

from typer import Option, Exit, prompt
from rich import print
from rich.panel import Panel

from ..tools.config_helpers import is_offline, get_config, remove_offline_files_list
from ..validators.github import validate_github_pat_token
from ..github.integrations import add_files_to_github


def publish(
        force: bool = Option(False, "--force", "-f", help="Publish files without prompting for confirmation")
) -> None:
    """
    Publishes files that were saved in offline mode using [bold cyan]qlm add[/bold cyan] :rocket:
    """

    if is_offline():
        print(Panel("[bold red1]You have to be in online mode to publish files to your remote repo. Connect with "
                    "[cyan]`qlm connect` :wink:"))
        raise Exit()

    try:
        files_to_publish: List[Dict[str, str]] = cast(List[Dict[str, str]], get_config(key="offline_files_to_add"))
        if len(files_to_publish) == 0:
            raise ValueError
    except ValueError:
        print(Panel("""[bold red1]You don't have any files to add in your config :cry:
You can check what's there using [cyan]qlm config[/cyan] and you can add files using [cyan]qlm add[/cyan] when in 
offline mode"""))
        raise Exit()

    github_token: str = validate_github_pat_token()
    if not force:
        filtered_files_to_show_user: List[Dict[str, str]] = [{"file": x["local_filepath"], "remote": x["remote"]} for x in files_to_publish]
        print(Panel(f"[bold green]You are going to publish the following files to github:[yellow]"
                             f"{filtered_files_to_show_user}"))
        answer: str = prompt("Do you wish to proceed? [y/n]")
        if answer != "y":
            raise Exit()

    asyncio.run(add_files_to_github(files_to_publish=files_to_publish, github_token=github_token))
    remove_offline_files_list()
