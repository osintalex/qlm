import os

from qlm.main import app
from qlm.tools.config_helpers import delete_config, set_config


def test_config(runner):
    result = runner.invoke(app, ["config"])
    assert result.exit_code == 0
    assert "{'offline': True, 'editor': 'vim'}\n" in result.stdout


def test_config_invalid_editor(runner):
    result = runner.invoke(app, ["config", "--editor", "i am not an editor"])
    assert result.exit_code == 0
    assert "The text editor i am not an editor is not an executable" in result.stdout


def test_config_editor(runner):
    result = runner.invoke(app, ["config", "--editor", "nano"])
    assert result.exit_code == 0
    assert "{'offline': True, 'editor': 'nano'}\n" in result.stdout
    set_config(key="editor", value="vim")


def test_config_invalid_empty_offline(runner):
    result = runner.invoke(app, ["config", "-eo"])
    assert result.exit_code == 0
    assert "You haven't set any offline files yet 😢" in result.stdout


def test_config_empty_offline(runner, offline_files):
    result = runner.invoke(app, ["config", "-eo"])
    assert result.exit_code == 0
    assert "{'offline': True, 'editor': 'vim'}\n" in result.stdout


def test_config_invalid_local_repo(runner):
    result = runner.invoke(app, ["config", "--local-repo", "i am a gaslighty path"])
    assert result.exit_code == 0
    assert "The path i am a gaslighty path does not exist ❌" in result.stdout


def test_config_local_repo(runner):
    result = runner.invoke(app, ["config", "--local-repo", os.getcwd()])
    assert result.exit_code == 0
    assert f"'local_repo': '{os.getcwd()}'" in result.stdout
    delete_config(key="local_repo")


def test_config_invalid_remote(runner):
    result = runner.invoke(app, ["config", "-rr", "not!allowed!&&"])
    assert result.exit_code == 0
    assert (
        "The remote not!allowed!&& contains characters that aren't allowed"
        in result.stdout
    )


def test_config_remote(runner):
    result = runner.invoke(app, ["config", "-rr", "permissible"])
    assert result.exit_code == 0
    assert "'remote_repo': 'permissible'}" in result.stdout
    delete_config(key="remote_repo")


def test_config_invalid_offline(runner):
    result = runner.invoke(app, ["config", "--offline", "0"])
    assert result.exit_code == 0
    assert (
        "You can only use True or False to set the offline configuration value!"
        in result.stdout
    )


def test_config_valid_offline(runner):
    result = runner.invoke(app, ["config", "--offline", "false"])
    assert result.exit_code == 0
    assert "{'offline': False," in result.stdout
    set_config(key="offline", value=True)
