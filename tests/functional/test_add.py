import os

from qlm.main import app
from qlm.tools.config_helpers import delete_config, get_config, show_configuration


def test_add_no_local(runner):
    result = runner.invoke(app, ["add", "humphrey.md"])
    assert result.exit_code == 0
    assert (
        f"Oh no 😟 You haven't yet set a value for the key local_repo" in result.stdout
    )


def test_add_no_matching_files(runner, local_repo):
    result = runner.invoke(app, ["add", "humphrey.md"])
    print(show_configuration())
    assert result.exit_code == 0
    assert f"No files matched the pattern humphrey.md" in result.stdout


def test_add_no_remote(runner, local_repo_with_file, fake_pat):
    result = runner.invoke(app, ["add", "humphrey.md"])
    assert result.exit_code == 0
    assert (
        f"Oh no 😟 You haven't yet set a value for the key remote_repo" in result.stdout
    )


def test_add_offline(runner, local_repo_with_file, remote_repo):
    result = runner.invoke(app, ["add", "humphrey.md", "--force"])
    assert result.exit_code == 0
    assert "Success" in result.stdout
    assert get_config(key="offline_files_to_add") == [
        {
            "repo_filepath": "humphrey.md",
            "local_filepath": os.path.join(local_repo_with_file, "humphrey.md"),
            "remote": remote_repo,
        }
    ]
    delete_config(key="offline_files_to_add")


def test_add_online_no_pat(runner, local_repo_with_file, remote_repo, online_mode):
    result = runner.invoke(app, ["add", "humphrey.md", "--force"])
    assert result.exit_code == 0
    assert "You didn't set the qlm_token environment variable" in result.stdout


def test_add_online(
    runner, local_repo_with_file, remote_repo, online_mode, fake_pat, mock_add_files
):
    result = runner.invoke(app, ["add", "humphrey.md", "--force"])
    assert result.exit_code == 0
    assert (
        "Successfully added files: ['humphrey.md'] to repo codevarna" in result.stdout
    )
