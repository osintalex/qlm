"""Module for interacting with the Github REST API."""

from base64 import b64encode
from typing import Dict, List, Optional

import httpx
from httpx import AsyncClient, Response
from rich import print
from rich.panel import Panel
from typer import Exit

from qlm.tools.config_helpers import set_config, show_configuration

github_json_type: str = "application/vnd.github+json"


def check_github_connection(github_token: str, remote: str) -> bool:
    """Tests that the user can connect to github.

    :param github_token: github PAT token.
    :param remote: path to the remote repo in format <user>/<repo name>
    :return: True if the connection is successful else False.
    :raise: exits with a bad API response.
    """

    response: Response = httpx.get(
        f"https://api.github.com/repos/{remote}",
        headers={"Authorization": f"token {github_token}", "Accept": github_json_type},
    )
    if response.status_code == 200:
        set_config(key="remote_repo", value=remote)
        return True
    if response.status_code == 404 and "/" not in remote:
        response = httpx.get(
            "https://api.github.com/user",
            headers={
                "Authorization": f"token {github_token}",
                "Accept": github_json_type,
            },
        )
        github_username: str = response.json()["login"]
        response = httpx.get(
            f"https://api.github.com/repos/{github_username}/{remote}",
            headers={
                "Authorization": f"token {github_token}",
                "Accept": github_json_type,
            },
        )
        if response.status_code != 200:
            print(
                Panel(
                    f"""[bold red1]Could not connect to repository [yellow]{remote}[/yellow] :x:
Error code : [bold cyan]{response.status_code}[/bold cyan]
Did you make sure to specify the full name of the repo in the [yellow]<username>/<repo>[/yellow] format?"""
                )
            )
            print(f"This is your current configuration: {show_configuration()}")
            raise Exit()
        set_config(key="remote_repo", value=f"{github_username}/{remote}")
        return True
    return False


def download_github_repository(github_token: str, remote: str) -> Response:
    """Downloads a github repository - equivalent to git clone.

    :param github_token: github PAT token.
    :param remote: path to the remote repo in format <user>/<repo name>
    :return: a zip archive.
    :raise: exits with a bad API response.
    """

    response: Response = httpx.get(
        f"https://api.github.com/repos/{remote}/zipball",
        headers={"Authorization": f"token {github_token}", "Accept": github_json_type},
        follow_redirects=True,
    )
    if response.status_code != 200:
        print(
            Panel(
                f"""[bold red1]Could not download from repository [yellow]{remote}[/yellow] :x:
Error code : [bold cyan]{response.status_code}[/bold cyan]"""
            )
        )
        print(f"This is your current configuration: {show_configuration()}")
        raise Exit()
    return response


def download_file(github_token: str, remote: str, file: str) -> Response:
    """Downloads a file from github.

    :param github_token: Github PAT token.
    :param remote: path to the remote repo in format <user>/<repo name>
    :param file: path to the file in the repo.
    :return: the file along with it's name.
    :raise: exits with a bad API response.
    """

    response: Response = httpx.get(
        f"https://api.github.com/repos/{remote}/contents/{file}",
        headers={"Authorization": f"token {github_token}", "Accept": github_json_type},
        follow_redirects=True,
    )
    if response.status_code != 200:
        print(
            Panel(
                f"""[bold red1]Could not get file[yellow]{file}[/yellow] :x:
Error code : [bold cyan]{response.status_code}[/bold cyan]"""
            )
        )
        print(f"This is your current configuration: {show_configuration()}")
        raise Exit()
    return response


def get_files_in_github_repo(
    github_token: str, remote: str, directory_path: str
) -> Response:
    """Lists files in the supplied path of a github repository.

    :param github_token: github PAT token.
    :param remote: path to the remote repo in format <user>/<repo name>
    :param directory_path: path to the directory in the repository.
    :return: a list of files in the directory.
    :raise: exits with a bad API response.
    """

    response: Response = httpx.get(
        f"https://api.github.com/repos/{remote}/contents/{directory_path}",
        headers={"Authorization": f"token {github_token}", "Accept": github_json_type},
    )
    if response.status_code != 200:
        print(
            f"[bold red]Oh no! :x: Could not get contents at {directory_path} in repo {remote}"
        )
        print(f"Error code: {response.status_code}")
        print(f"This is your current configuration: {show_configuration()}")
        print(
            Panel(
                f"[bold red1]Could not get contents at [yellow]{directory_path}[/yellow] in repo "
                f"[yellow]{remote}[/yellow] :x: Error code : [bold cyan]{response.status_code}[/bold cyan]"
            )
        )
        print(f"This is your current configuration: {show_configuration()}")
        raise Exit()
    return response


def delete_file(github_token: str, remote: str, file_path: str) -> None:
    """Deletes a file in the github repository.

    :param github_token: github PAT token.
    :param remote: path to the remote repo in format <user>/<repo name>
    :param file_path: path to the file to delete.
    :raise: Exits the program in case it can't get the hash which is required to delete the file from the remote.
    """

    response: Response = httpx.get(
        f"https://api.github.com/repos/{remote}/contents/{file_path}",
        headers={"Authorization": f"token {github_token}", "Accept": github_json_type},
        follow_redirects=True,
    )
    if response.status_code != 200:
        print(
            Panel(
                f"""[bold red1]Could not get file hash for file [yellow]{file_path}[/yellow] :x:
This is required to delete the file :cry:
Error code : [bold cyan]{response.status_code}[/bold cyan]"""
            )
        )
        print(f"This is your current configuration: {show_configuration()}")
        raise Exit()
    file_sha_value: str = response.json()["sha"]
    response = httpx.request(
        method="delete",
        url=f"https://api.github.com/repos/{remote}/contents/{file_path}",
        headers={"Authorization": f"token {github_token}", "Accept": github_json_type},
        json={
            "message": ":pen: deleted by qlm",
            "sha": file_sha_value,
        },
    )
    if response.status_code != 200:
        print(
            Panel(
                f"[bold red1]Could not get delete file [yellow]{file_path}[/yellow] in repo"
                f"[yellow]{remote}[/yellow] :x: Error code : [bold cyan]{response.status_code}[/bold cyan]"
            )
        )
        print(f"This is your current configuration: {show_configuration()}")


def create_new_repo(repo_name: str, public: bool, github_token: str) -> str:
    """Creates a new github repository.

    :param repo_name: the name of the repository.
    :param public: whether the new repo should be public.
    :param github_token: github PAT token.
    :return: full name of the repo
    :raise: Exits in case of an API error.
    """

    response: Response = httpx.post(
        "https://api.github.com/user/repos",
        headers={"Authorization": f"token {github_token}", "Accept": github_json_type},
        json={"name": repo_name, "private": not public},
    )
    if response.status_code not in {200, 201}:
        print(
            Panel(
                f"""[bold red1]Could not create new repository [yellow]{repo_name}[/yellow] :x:
Error code : [bold cyan]{response.status_code}[/bold cyan]"""
            )
        )
        raise Exit()
    return response.json()["full_name"]


async def add_files_to_github(
    files_to_publish: List[Dict[str, str]], github_token: str
) -> None:
    """Add files to github.

    :param files_to_publish: list of files to publish and respective information required to publish them, i.e.
    path relative to the remote and which remote to publish them to.
    :param github_token: github PAT token.
    :raise: Exits in case of an API error.
    """

    async with AsyncClient() as client:
        for x in files_to_publish:
            request_url: str = f"https://api.github.com/repos/{x['remote']}/contents/{x['repo_filepath']}"
            with open(x["local_filepath"], "rb") as f:
                file_content: str = b64encode(f.read()).decode()
            file_sha: Optional[str] = await generate_file_sha_if_needed(
                repo_filepath=x["repo_filepath"],
                remote=x["remote"],
                github_token=github_token,
            )
            payload: Dict[str, str] = {
                "message": ":pen: added by qlm",
                "content": file_content,
            }
            if file_sha:
                payload["sha"] = file_sha
            response: Response = await client.put(
                url=request_url,
                headers={
                    "Authorization": f"token {github_token}",
                    "Accept": github_json_type,
                },
                json=payload,
            )
            if response.status_code not in {200, 201}:
                print(
                    Panel(
                        f"""[bold red1]Could not add file [yellow]{x['repo_filepath']}[/yellow]:x:
Error code : [bold cyan]{response.status_code}[/bold cyan]"""
                    )
                )
                raise Exit()


async def generate_file_sha_if_needed(
    repo_filepath: str, remote: str, github_token: str
) -> Optional[str]:
    """Generates the sha of a file in github if and only if the file is already in github, i.e. it will return None
    if the file is not already in github.

    :param repo_filepath: Path to the file relative to the repo root.
    :param remote: the remote repos in format <user>/<repo name>
    :param github_token: github PAT token.
    :return: The file sha if the file is in github.
    """

    async with AsyncClient() as client:
        request_url: str = (
            f"https://api.github.com/repos/{remote}/contents/{repo_filepath}"
        )
        response: Response = await client.get(
            url=request_url,
            headers={
                "Authorization": f"token {github_token}",
                "Accept": github_json_type,
            },
        )
        if response.status_code == 200:
            return response.json()["sha"]
    return None
