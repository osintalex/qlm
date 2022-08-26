from qlm.main import app

from qlm.tools.config_helpers import delete_config


def test_publish_offline(runner):
    result = runner.invoke(app, ["publish"])
    assert result.exit_code == 0
    assert "You have to be in online mode to publish files to your remote repo." in result.stdout


def test_publish_no_token(runner, online_mode, offline_files):
    result = runner.invoke(app, ["publish"])
    assert result.exit_code == 0
    assert "You didn't set the qlm_token environment variable" in result.stdout
    delete_config(key="offline_files_to_add")


def test_publish(runner, online_mode, offline_files, fake_pat, mock_publish_files):
    result = runner.invoke(app, ["publish", "-f"])
    assert result.exit_code == 0
    assert "Successfully published files to github" in result.stdout
