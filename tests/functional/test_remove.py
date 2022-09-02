from qlm.main import app


def test_remove_invalid_file(runner, local_repo):
    result = runner.invoke(app, ["rm", "invisible.md", "--force"])
    assert result.exit_code == 0
    assert "This file" and "doesn't exist 😢" in result.stdout


def test_remove_file(runner, local_repo_with_file):
    result = runner.invoke(app, ["rm", "humphrey.md", "--force"])
    assert result.exit_code == 0
    assert "Successfully deleted file humphrey.md 💥" in result.stdout


def test_remove_online_file_no_token(runner, online_mode):
    result = runner.invoke(app, ["rm", "je suis online.md", "--force"])
    assert result.exit_code == 0
    assert "You didn't set the qlm_token environment variable" in result.stdout


def test_remove_online_file_no_remote(runner, online_mode, fake_pat):
    result = runner.invoke(app, ["rm", "je suis online.md", "--force"])
    assert result.exit_code == 0
    assert (
        "Oh no 😟 You haven't yet set a value for the key remote_repo" in result.stdout
    )


def test_remove_online_file_no_remote(
    runner, online_mode, fake_pat, remote_repo, mock_delete_file
):
    result = runner.invoke(app, ["rm", "je suis online.md", "--force"])
    assert result.exit_code == 0
    assert "Successfully deleted file je suis online.md 💥" in result.stdout
