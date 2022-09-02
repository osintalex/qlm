from qlm.main import app
from qlm.tools.config_helpers import set_config


def test_connect_no_token(runner):
    result = runner.invoke(app, ["connect", "codevarna"])
    assert result.exit_code == 0
    assert "You didn't set the qlm_token environment variable" in result.stdout


def test_connect_bad_repo(runner, fake_pat):
    result = runner.invoke(app, ["connect", "3vilr3p0!!"])
    assert result.exit_code == 0
    assert "The remote name 3vilr3p0!! is not allowed by github 😢" in result.stdout
    set_config(key="offline", value=True)


def test_good_connect(runner, fake_pat, mock_check_github_connection):
    mock_check_github_connection.return_value = True
    result = runner.invoke(app, ["connect", "code-goodness"])
    assert result.exit_code == 0
    assert (
        "Success! You are connected to github repository code-goodness 💥"
        in result.stdout
    )
    set_config(key="offline", value=True)


def test_bad_connect(runner, fake_pat, mock_check_github_connection):
    mock_check_github_connection.return_value = False
    result = runner.invoke(app, ["connect", "code-goodness"])
    assert result.exit_code == 0
    assert "Could not connect to github repository code-goodness 😢" in result.stdout
    set_config(key="offline", value=True)
