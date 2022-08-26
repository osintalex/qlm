from qlm.main import app

from qlm.tools.config_helpers import set_config, delete_config


def test_create_no_token(runner):
    result = runner.invoke(app, ["create", "codevarna", "--force"])
    assert result.exit_code == 0
    assert "You didn't set the qlm_token environment variable" in result.stdout


def test_create_bad_repo(runner, fake_pat):
    result = runner.invoke(app, ["create", "codevarna!!", "--force"])
    assert result.exit_code == 0
    assert "The remote name codevarna!! is not allowed by github 😢" in result.stdout
    set_config(key="offline", value=True)


def test_create_good_repo(runner, fake_pat, mock_repo_creation):
    result = runner.invoke(app, ["create", "codevarna", "--force"])
    assert result.exit_code == 0
    assert f"You are now in online mode and connected to github repository codevarna" in result.stdout
    set_config(key="offline", value=True)
    delete_config(key="remote_repo")
