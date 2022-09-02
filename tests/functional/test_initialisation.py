from qlm.main import app


def test_help_on_startup(runner):
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert " Usage: root [OPTIONS] COMMAND [ARGS]..." in result.stdout
    for x in {
        "add",
        "config",
        "connect",
        "create",
        "download",
        "edit",
        "get",
        "ls",
        "offline",
        "publish",
        "rm",
        "show",
    }:
        assert x in result.stdout
