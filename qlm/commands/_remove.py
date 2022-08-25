from os import path, remove

from typer import Argument, Option, Exit, prompt
from rich import print
from rich.panel import Panel

from qlm.tools.config_helpers import is_offline, get_config
from qlm.validators.github import validate_github_pat_token
from qlm.validators.files import validate_file_exists
from qlm.github.integrations import delete_file


def rm(file: str = Argument(..., help="The file you want to remove"),
       force: bool = Option(False, "--force", "-f", help="Remove the file without prompting for confirmation")
       ) -> None:
    """
    Removes a file :smiling_imp:
    """

    if is_offline():
        local_repo: str = get_config(key="local_repo")
        path_to_file: str = path.join(local_repo, file)
        validate_file_exists(path_to_file=path_to_file)
        if not force:
            answer: str = prompt(f"Are you sure you want to delete the file {file}? [y/n]")
            if answer != "y":
                raise Exit()
        remove(path_to_file)
    else:
        if not force:
            answer: str = prompt(f"Are you sure you want to delete the file {file}? [y/n]")
            if answer != "y":
                raise Exit()
        github_token: str = validate_github_pat_token()
        remote: str = get_config(key="remote_repo")
        delete_file(github_token=github_token, remote=remote, file_path=file)
    print(Panel(f"[bold green]Successfully deleted file [yellow]{file} :boom:"))