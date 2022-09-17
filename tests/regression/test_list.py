from qlm.main import app


def test_list_with_directories(
    runner, fake_pat, online_mode, remote_repo, mock_get_files
):
    """Previous bug - results didn't include directories"""

    class DummyResponse:
        @staticmethod
        def json():
            return [
                {"name": "peeka.md", "type": "file"},
                {"name": "boo", "type": "dir"},
            ]

    mock_get_files.return_value = DummyResponse
    result = runner.invoke(app, ["ls"])
    assert result.exit_code == 0
    assert "['peeka.md', 'boo/']" in result.stdout
