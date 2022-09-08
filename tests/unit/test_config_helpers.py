from click.exceptions import Exit

from qlm.tools.config_helpers import delete_config


def test_delete_config(capsys):
    try:
        delete_config(key="I don't exist")
    except Exit:
        assert "You haven't set the key I don't exist yet" in capsys.readouterr().out
