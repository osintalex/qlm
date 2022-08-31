from typing import Dict, List, Union, NewType, Optional
from os import path
import json

from rich import print
from rich.panel import Panel
from typer import Exit

config_filepath: str = path.join(path.dirname(__file__), 'config.json')
CONFIG_TYPE = NewType("CONFIG_TYPE", Dict[str, Union[str, bool, List[Dict[str, str]]]])


def is_offline() -> bool:
    """Checks if qlm is running in offline mode or not.

    :return: True if it else else False.
    """

    with open(config_filepath, "r") as f:
        config_data: CONFIG_TYPE = json.load(f)
    return config_data["offline"]


def set_config(key: str, value: Union[str, bool, List[Dict[str, str]]]) -> None:
    """Utility function to set a given key value pair in the config.

    :param key: the name of the config key to set the value of.
    :param value: the value to set it to.
    """

    with open(config_filepath, "r") as f:
        config_data: CONFIG_TYPE = json.load(f)
    config_data[key] = value
    with open(config_filepath, "w") as f:
        json.dump(config_data, f)


def get_config(key: str) -> Optional[Union[str, bool, List[Dict[str, str]]]]:
    """Utility function to get a given key value in the config.

    :param key: name of the key to get the value of.
    :return: the key's value.
    :raise: Exits the program if the key doesn't exist.
    """
    with open(config_filepath, "r") as f:
        config_data: CONFIG_TYPE = json.load(f)
    try:
        return config_data[key]
    except KeyError:
        print(Panel(f"[bold red1]Oh no :worried: You haven't yet set a value for the key [cyan]{key}"))
        raise Exit


def delete_config(key: str) -> None:
    """Utility function to remove a given key's value from the config.

    :param key: the name of the config key to set the value of.
    :raise: Exits the program if the key doesn't exist.
    """

    with open(config_filepath, "r") as f:
        config_data: CONFIG_TYPE = json.load(f)
    try:
        config_data.pop(key)
    except KeyError:
        print(Panel(f"[bold red1]You haven't set the key {key} yet :cry:"))
        raise Exit()
    with open(config_filepath, "w") as f:
        json.dump(config_data, f)


def show_configuration(hide_key: str = None) -> CONFIG_TYPE:
    """Utility method to get the contents of the `config.json` file.

    :param hide_key: key to mask from output
    :return: Dictionary containing the configuration values.
    """

    with open(config_filepath, "r") as f:
        config_data: CONFIG_TYPE = json.load(f)
        if hide_key:
            config_data.pop(hide_key)
        return config_data


def make_note_to_add_files_later(repo_path_to_files: List[str],
                                 local_file_paths: List[str],
                                 remotes: List[str]) -> None:
    """Makes a note to add a file later to github using the `qlm publish` command.

    :param repo_path_to_files: paths relative to the repo root, i.e. what the will be in github.
    :param local_file_paths: paths in current local directory.
    :param remotes: The name of the remotes in which you want to add the file; has format <username>/<remote>.
    """

    with open(config_filepath, "r") as f:
        config_data: CONFIG_TYPE = json.load(f)
        new_information: List[Dict[str, str]] = [{"repo_filepath": x, "local_filepath": y, "remote": z}
                                                 for x, y, z in zip(repo_path_to_files, local_file_paths, remotes)]
    if not config_data.get("offline_files_to_add"):
        config_data["offline_files_to_add"] = new_information
    else:
        config_data["offline_files_to_add"] = config_data["offline_files_to_add"] + new_information
    with open(config_filepath, "w") as f:
        json.dump(config_data, f)


def remove_offline_files_list() -> None:
    """Removes the current list of offline files to be added later.

    :raise: Exits the program if the key doesn't exist.
    """

    with open(config_filepath, "r") as f:
        config_data: CONFIG_TYPE = json.load(f)
    try:
        config_data.pop("offline_files_to_add")
    except KeyError:
        print(Panel("[bold red1]You haven't set any offline files yet :cry:"))
        raise Exit
    with open(config_filepath, "w") as f:
        json.dump(config_data, f)
