from os import path
from base64 import b64decode

from typer import Argument, Option, Exit
from rich import print
from rich.console import Console
from rich.markdown import Markdown
from httpx import Response

from ..tools.config_helpers import is_offline, get_config
from ..validators.github import validate_github_pat_token
from ..github.integrations import download_file

console = Console()


def show(file: str = Argument(..., help="The path to the file you want see."),
         no_markdown: bool = Option(False, "--no-markup", "-nm", help="Print a file out without rendering markdown.")
         ) -> None:
    """
    Prints your file to the console. Looks much nicer if you use markdown :innocent:
    """

    if is_offline():
        local_repo: str = get_config(key="local_repo")
        path_to_local_file: str = path.join(local_repo, file)
        if not path.exists(path_to_local_file):
            print(f"Hey dickhead there is nothing at {path_to_local_file}")
            raise Exit()
        with open(path_to_local_file, "r") as f:
            file_contents: str = f.read()
    else:
        remote: str = get_config(key="remote_repo")
        github_token: str = validate_github_pat_token()
        response: Response = download_file(github_token=github_token, remote=remote, file=file)
        file_contents: str = b64decode(response.json()["content"]).decode()

    if no_markdown:
        print(file_contents)
    else:
        rendered_markdown: Markdown = Markdown(file_contents)
        console.print(rendered_markdown)
