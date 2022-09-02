import os
import shutil

from qlm.main import app


def test_download_while_offline(runner, local_repo):
    result = runner.invoke(app, ["download", local_repo.name])
    assert result.exit_code == 0
    assert "You are not in online mode 😢" in result.stdout


def test_download_no_token(runner, local_repo, online_mode):
    result = runner.invoke(app, ["download", local_repo.name])
    assert result.exit_code == 0
    assert "You didn't set the qlm_token environment variable" in result.stdout


def test_download_bad_remote(runner, local_repo, online_mode, fake_pat):
    result = runner.invoke(
        app, ["download", local_repo.name, "--remote", "b4d!!!r3mot3t&&"]
    )
    assert result.exit_code == 0
    assert (
        "The characters in b4d!!!r3mot3t&& are not allowed by github 😢" in result.stdout
    )


def test_download_bad_remote(
    runner,
    local_repo_with_file,
    online_mode,
    fake_pat,
    remote_repo,
    mock_download_github_repository,
):
    shutil.make_archive(
        os.path.join(local_repo_with_file, "123"), "zip", local_repo_with_file
    )
    with open(os.path.join(local_repo_with_file, "123.zip"), "rb") as f:
        bytes_content = f.read()

    class DummyResponse:
        content = bytes_content

    mock_download_github_repository.return_value = DummyResponse
    result = runner.invoke(app, ["download", local_repo_with_file])
    assert result.exit_code == 0
    assert "Successfully downloaded repo to directory:" in result.stdout
