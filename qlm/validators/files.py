from os import path

from typer import Exit
from rich import print
from rich.panel import Panel


def validate_file_path_is_empty(filepath: str):
    """Validates that a local file path is empty.

    :param filepath: the filepath to check.
    :return: True if the file is empty.
    :raise: Quits the program if validation files.
    """

    if path.exists(filepath):
        print(f"Yo dumbass there is already a file at {filepath}")
        raise Exit()


def validate_file_exists(path_to_file: str):
    """Validates that a local file exists and is not a directory.

    :param path_to_file: path to the file.
    :raise: Quits the program if validation fails.
    """

    if not path.exists(path_to_file):
        print(Panel(f"[bold red1]This file: [yellow]{path_to_file}[/yellow] doesn't exist :cry:"))
        raise Exit()
    if path.isdir(path_to_file):
        print(Panel(f"[bold red1] This is a directory not a file:  [yellow]{path_to_file}[/yellow] :cry:"))
        raise Exit()
