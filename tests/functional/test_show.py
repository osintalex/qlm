
from qlm.main import app


def test_show_no_local(runner):
    result = runner.invoke(app, ["show", "nada.md"])
    assert result.exit_code == 0
    assert "Oh no 😟 You haven't yet set a value for the key local_repo" in result.stdout


def test_show_bad_file(runner, local_repo):
    result = runner.invoke(app, ["show", "nada.md"])
    assert result.exit_code == 0
    assert "The file nada.md does not exist 😭" in result.stdout


def test_show_bad_file(runner, local_repo_with_file):
    result = runner.invoke(app, ["show", "humphrey.md"])
    assert result.exit_code == 0
    assert "Testing" in result.stdout


def test_show_online_no_remote(runner, online_mode):
    result = runner.invoke(app, ["show", "the life of pi.md"])
    assert result.exit_code == 0
    assert "Oh no 😟 You haven't yet set a value for the key remote_repo" in result.stdout


def test_show_online_no_remote(runner, online_mode, remote_repo):
    result = runner.invoke(app, ["show", "the life of pi.md"])
    assert result.exit_code == 0
    assert "You didn't set the qlm_token environment variable" in result.stdout


def test_show_online_no_remote(runner, online_mode, remote_repo, fake_pat, mock_download_file_for_show):
    class DummyResponse:
        @staticmethod
        def json():
            return {"content": b'I0V4Y2VsbGVudA=='}
    mock_download_file_for_show.return_value = DummyResponse
    result = runner.invoke(app, ["show", "the life of pi.md"])
    assert result.exit_code == 0
    assert "Excellent" in result.stdout