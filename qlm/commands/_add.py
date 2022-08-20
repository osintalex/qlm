from os import path
from glob import glob
from typing import List, Dict
import asyncio

from typer import Argument, Option, Exit, prompt
from rich import print
from rich.panel import Panel

from ..tools.config_helpers import is_offline, get_config, make_note_to_add_files_later
from ..validators.github import validate_github_pat_token
from ..github.integrations import add_files_to_github


def add(files: str = Argument(..., help="The path to the file you want to add. Accepts wildcard syntax, "
                                        "i.e. [yellow]myfolder/*.md"),
        force: bool = Option(False, "--force", "-f", help="Don't prompt before adding files")
        ) -> None:
    """
    Add file(s) to your github remote from your local repo. Accepts wildcards with glob syntax like [yellow]'*.md'[/yellow].

    If you're offline, qlm records this in your configuration. You can see which files qlm has stored by running [bold cyan]qlm config[/bold cyan].

    You can add them all to github later by running [bold cyan]qlm publish[/bold cyan].

    You can empty this list of files by running [bold cyan]qlm config --empty-offline[/bold cyan]. Or you can use [hot_pink]git[/hot_pink] yourself to send files to your remote!
    """

    local_repo: str = get_config(key="local_repo")
    files_to_add: List[str] = glob(path.join(local_repo, files))
    if not files_to_add:
        print(Panel(f"""No files matched the pattern [yellow]{files}[/yellow] :worried:
                    
Have you set your local repo correctly? You can set it with [bold cyan]qlm config -lr"""))
        raise Exit()
    if is_offline():
        remote: str = get_config("remote_repo")
        remotes: List[str] = [remote] * len(files_to_add)
        repo_path_to_files: List[str] = [path.relpath(x, local_repo) for x in files_to_add]
        if not force:
            print(Panel(f"[bold green]You are saving these files to add to your remote {remote} later:[/bold green] [yellow]{files_to_add}"))
            answer: str = prompt("Do you wish to proceed? [y/n]")
            if answer != "y":
                raise Exit()
        make_note_to_add_files_later(repo_path_to_files=repo_path_to_files,
                                     local_file_paths=files_to_add, remotes=remotes)
        print(Panel(f"[bold green]Success! Made a note to add files:[/bold green] [yellow]{files_to_add}[/yellow] [bold green]to the remote[/bold green] [hot_pink]{remote}"))
    else:
        github_token: str = validate_github_pat_token()
        remote: str = get_config(key="remote_repo")
        files_to_add_relative_to_repo_root: List[str] = [path.relpath(x, local_repo) for x in files_to_add]
        if not force:
            print(Panel(f"[bold green]You are about to add these files to [cyan]{remote}[/cyan] on github: [yellow]{files_to_add_relative_to_repo_root}"))
            answer: str = prompt("Do you wish to proceed? [y/n]")
            if answer != "y":
                raise Exit()
        remotes: List[str] = [remote] * len(files_to_add_relative_to_repo_root)
        files_to_publish: List[Dict[str, str]] = [{"repo_filepath": x, "local_filepath": y, "remote": z} for
                                                  x, y, z in zip(files_to_add_relative_to_repo_root, files_to_add, remotes)]
        asyncio.run(add_files_to_github(files_to_publish=files_to_publish, github_token=github_token))
        print(Panel(f"[bold green]Successfully added files: [/bold green][yellow]{files_to_add_relative_to_repo_root}[/yellow] [bold green]to repo[/bold green] [hot_pink]{remote}"))
