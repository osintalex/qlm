import os
from tempfile import TemporaryDirectory

import pytest

from qlm.main import app


def test_get_offline(runner):
    result = runner.invoke(app, ["get", "woops.md"])
    assert result.exit_code == 0
    assert "This is an online only command 😭" in result.stdout


def test_get_no_pat(runner, online_mode):
    result = runner.invoke(app, ["get", "woops.md"])
    assert result.exit_code == 0
    assert "You didn't set the qlm_token environment variable" in result.stdout


def test_get_no_remote(runner, online_mode, fake_pat):
    result = runner.invoke(app, ["get", "woops.md"])
    assert result.exit_code == 0
    assert (
        "Oh no 😟 You haven't yet set a value for the key remote_repo" in result.stdout
    )


def test_get_overwrite_disallowed(
    runner, online_mode, fake_pat, remote_repo, mock_download_file_for_get
):
    filename = "please don't overwrite me.md"
    cwd = os.getcwd()
    filepath = os.path.join(cwd, filename)

    class DummyResponse:
        @staticmethod
        def json():
            return {"content": b"YWJj", "name": filename}

    mock_download_file_for_get.return_value = DummyResponse
    with open(filepath, "w") as f:
        f.write("placeholder")
    result = runner.invoke(app, ["get", "woops.md"])
    assert result.exit_code == 0
    assert "There is already a file at:" in result.stdout
    os.remove(filepath)


def test_get_success(
    runner, online_mode, fake_pat, remote_repo, mock_download_file_for_get
):
    filename = "my cool new file.md"
    cwd = os.getcwd()
    filepath = os.path.join(cwd, filename)

    class DummyResponse:
        @staticmethod
        def json():
            return {"content": b"YWJj", "name": filename}

    mock_download_file_for_get.return_value = DummyResponse
    result = runner.invoke(app, ["get", filename])
    assert result.exit_code == 0
    assert "Success! You downloaded file my cool new file.md" in result.stdout
    assert os.path.exists(filepath)
    os.remove(filepath)


def test_get_success(
    runner, online_mode, fake_pat, remote_repo, mock_download_file_for_get
):
    filename = "my cool new file.md"
    cwd = os.getcwd()
    filepath = os.path.join(cwd, filename)

    class DummyResponse:
        @staticmethod
        def json():
            return {"content": b"YWJj", "name": filename}

    mock_download_file_for_get.return_value = DummyResponse
    result = runner.invoke(app, ["get", filename])
    assert result.exit_code == 0
    assert "Success! You downloaded file my cool new file.md" in result.stdout
    assert os.path.exists(filepath)
    os.remove(filepath)


@pytest.mark.parametrize(
    "rename, directory",
    [
        ("new file.md", TemporaryDirectory()),
        ("", TemporaryDirectory()),
        ("new file.md", ""),
    ],
)
def test_get_success_filepath_and_name_combinations(
    rename,
    directory,
    runner,
    online_mode,
    fake_pat,
    remote_repo,
    mock_download_file_for_get,
):
    filename = rename if rename else "my cool new file.md"
    chosen_directory = directory.name if directory else os.getcwd()
    filepath = os.path.join(chosen_directory, filename)

    class DummyResponse:
        @staticmethod
        def json():
            return {"content": b"YWJj", "name": filename}

    mock_download_file_for_get.return_value = DummyResponse
    if rename and directory:
        result = runner.invoke(
            app, ["get", filename, "--rename", rename, "--directory", chosen_directory]
        )
    if directory and not rename:
        result = runner.invoke(app, ["get", filename, "--directory", chosen_directory])
    if rename and not directory:
        result = runner.invoke(app, ["get", filename, "--rename", rename])
    assert result.exit_code == 0
    assert f"Success! You downloaded file {filename}" in result.stdout
    assert os.path.exists(filepath)
    os.remove(filepath)
    if directory:
        directory.cleanup()
