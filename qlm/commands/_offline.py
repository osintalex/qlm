import os

from typer import Argument, Exit
from rich import print
from rich.panel import Panel

from qlm.tools.config_helpers import set_config


def offline(local: str = Argument(..., help="The absolute path to the local directory where you want to keep "
                                            "your notes")) -> None:
    """
    Switch to working in offline mode with a local directory :shuffle_tracks_button:

    If you want to add your work to a remote later, use qlm publish.
    """

    current_working_directory: str = os.getcwd()
    if not os.path.isdir(local):
        print(Panel(f"[bold red1]The directory [cyan]{local}[/cyan] does not exist!"))
        raise Exit()

    try:
        os.chdir(local)
    except PermissionError:
        print(Panel(f"[bold red1]You do not have permissions to work in the directory [cyan]{local}"))
        raise Exit()

    os.chdir(current_working_directory)
    set_config(key="offline", value=True)
    set_config(key="local_repo", value=local)
    print(Panel(f"""[bold green]Now working offline in local directory: [yellow]{local}[/yellow] :smile:
Go back online by running [cyan]qlm connect :thumbs_up:"""))
