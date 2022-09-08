from qlm.main import app
from qlm.tools.config_helpers import set_config


def test_config_in_online_mode(runner):
    """Previous bug - if you were in online mode, `qlm config` would always say you were offline."""
    set_config(key="offline", value=False)
    result = runner.invoke(app, ["config"])
    assert result.exit_code == 0
    assert "{'offline': False, 'editor': 'vim'}\n" in result.stdout
    set_config(key="offline", value=True)
