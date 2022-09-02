import os

from qlm.main import app


def test_edit_no_local(runner):
    result = runner.invoke(app, ["edit", "mypreciousfile.md"])
    assert result.exit_code == 0
    assert "Oh no 😟 You haven't yet set a value for the key local_repo" in result.stdout


def test_edit_non_existent_file(runner, local_repo):
    result = runner.invoke(app, ["edit", "misleading.md"])
    assert result.exit_code == 0
    assert "The file misleading.md doesn't exist 😕" in result.stdout


def test_edit_directory(runner, local_repo):
    result = runner.invoke(app, ["edit", local_repo.name])
    assert result.exit_code == 0
    assert "directory not a file 😕" in result.stdout


def test_edit_offline(runner, local_repo_with_file, mock_call_to_editor):
    result = runner.invoke(app, ["edit", "humphrey.md"])
    filepath = os.path.join(local_repo_with_file, "humphrey.md")
    assert result.exit_code == 0
    mock_call_to_editor.assert_called_once_with(f"vim {filepath}")


def test_edit_online_no_token(runner, online_mode):
    result = runner.invoke(app, ["edit", "magicfile.md"])
    assert result.exit_code == 0
    assert "You didn't set the qlm_token environment variable" in result.stdout


def test_edit_online_no_remote(runner, online_mode, fake_pat):
    result = runner.invoke(app, ["edit", "magicfile.md"])
    assert result.exit_code == 0
    assert (
        "Oh no 😟 You haven't yet set a value for the key remote_repo" in result.stdout
    )


def test_edit_online(
    runner,
    online_mode,
    fake_pat,
    remote_repo,
    mock_call_to_editor,
    mock_download_file_for_edit,
    mock_add_files_after_editing,
):
    class DummyResponse:
        @staticmethod
        def json():
            return {"content": b"YWJj"}

    mock_download_file_for_edit.return_value = DummyResponse
    result = runner.invoke(app, ["edit", "magicfile.md"])
    assert result.exit_code == 0
    mock_call_to_editor.assert_called_once()
    mock_add_files_after_editing.assert_called_once()
