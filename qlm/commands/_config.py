from typer import Option, Exit
from rich import print
from rich.panel import Panel

from qlm.tools.config_helpers import show_configuration, set_config, remove_offline_files_list
from qlm.validators.config import must_be_executable, path_must_exist, must_be_allowed_by_github, validate_offline_flag


def config(editor: str = Option("", "--editor", "-e", help="The command to open the text editor you want to use, i.e. "
                                                           "[bold cyan]nano[/bold cyan] or [bold cyan]vim[/bold cyan]"),
           empty_offline: bool = Option(False, "--empty-offline", "-eo", help="Empty the list of offline files to add "
                                                                              "with [bold cyan]qlm publish[/bold cyan]. If you want more "
                                                                              "granular control of these files, it's "
                                                                              "probably best to empty them and then "
                                                                              "manually add them to them github using "
                                                                              "[hot_pink]git[/hot_pink] on the command line"),
           local_repo: str = Option("", "--local-repo", "-lr", help="The absolute path to the local directory you want "
                                                                    "to keep your files in."),
           remote_repo: str = Option("", "--remote-repo", "-rr", help="The full name of the remote repo you want to "
                                                                      "use, i.e. <username>/<repo>"),
           hide_key: str = Option("", "--hide-key", "-hk", help="Don't print out a specific key in the configuration "
                                                                "output"),
           offline: str = Option(True, "--offline", "-o", help="Set offline to True or False. Defaults to True."),

           ) -> None:
    """
    Display and edit your current configuration :zap:

    """
    if editor:
        try:
            must_be_executable(editor)
        except ValueError:
            print(Panel(f"[bold red1]The text editor [cyan]{editor}[/cyan] is not an executable"))
            raise Exit()
        set_config(key="text_editor", value=editor)
    if empty_offline:
        remove_offline_files_list()
    if local_repo:
        try:
            path_must_exist(local_repo)
        except ValueError:
            print(Panel(f"[bold red1]The path [cyan]{local_repo}[/cyan] does not exist"))
            raise Exit()
        set_config(key="local_repo", value=local_repo)
    if remote_repo:
        try:
            must_be_allowed_by_github(remote_repo)
        except ValueError:
            print(Panel(f"""[bold red1]The remote [cyan]{remote_repo}[/cyan] contains characters that aren't allowed by
github. You can only use latin letters, numbers, forward slashes, underscores, full stops and hyphens"""))
            raise Exit()
        set_config(key="remote_repo", value=remote_repo)
    if offline:
        try:
            validated: bool = validate_offline_flag(value=offline)
        except ValueError:
            print(Panel("[bold red1]You can only use [cyan]True[/cyan] or [cyan]False[/cyan] to set the offline "
                        "configuration value!"))
            raise Exit()
        set_config(key="offline", value=validated)
    print(show_configuration(hide_key=hide_key))
