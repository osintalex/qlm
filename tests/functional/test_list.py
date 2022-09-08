from qlm.main import app


def test_list_offline(runner):
    result = runner.invoke(app, ["ls"])
    assert result.exit_code == 0
    assert "You aren't connected to a remote." in result.stdout


def test_list_file_request(runner, fake_pat, online_mode, remote_repo, mock_get_files):
    class DummyResponse:
        @staticmethod
        def json():
            return "hello i'm a file"

    mock_get_files.return_value = DummyResponse
    result = runner.invoke(app, ["ls", "ceci est un file"])
    assert result.exit_code == 0
    assert "The argument ceci est un file is a file" in result.stdout


def test_list_markdown(runner, fake_pat, online_mode, remote_repo, mock_get_files):
    class DummyResponse:
        @staticmethod
        def json():
            return [{"name": "peeka.md"}, {"name": "boo.md"}]

    mock_get_files.return_value = DummyResponse
    result = runner.invoke(app, ["ls", "ceci n'est pas un file"])
    assert result.exit_code == 0
    assert "['peeka.md', 'boo.md']" in result.stdout


def test_list_markdown_no_input(
    runner, fake_pat, online_mode, remote_repo, mock_get_files
):
    class DummyResponse:
        @staticmethod
        def json():
            return [{"name": "peeka.md"}, {"name": "boo.md"}]

    mock_get_files.return_value = DummyResponse
    result = runner.invoke(app, ["ls"])
    assert result.exit_code == 0
    assert "['peeka.md', 'boo.md']" in result.stdout


def test_list_non_markdown(runner, fake_pat, online_mode, remote_repo, mock_get_files):
    class DummyResponse:
        @staticmethod
        def json():
            return [{"name": "peeka.md"}, {"name": "chu"}]

    mock_get_files.return_value = DummyResponse
    result = runner.invoke(app, ["ls", "ceci n'est pas un file", "-nm"])
    assert result.exit_code == 0
    assert "['peeka.md', 'chu']" in result.stdout
