import os
from tempfile import TemporaryDirectory
from asyncio import coroutine, run

import pytest
from typer.testing import CliRunner

from qlm.tools.config_helpers import set_config, delete_config


@pytest.fixture
def runner():
    yield CliRunner()


@pytest.fixture
def local_repo():
    tmpdir = TemporaryDirectory()
    set_config(key="local_repo", value=tmpdir.name)
    yield tmpdir
    tmpdir.cleanup()
    delete_config(key="local_repo")


@pytest.fixture
def local_repo_with_file():
    tmpdir = TemporaryDirectory()
    set_config(key="local_repo", value=tmpdir.name)
    with open(os.path.join(tmpdir.name, "humphrey.md"), "w") as f:
        f.write("# Testing")
    yield tmpdir.name
    tmpdir.cleanup()
    delete_config(key="local_repo")


@pytest.fixture
def remote_repo():
    set_config(key="remote_repo", value="codevarna")
    yield "codevarna"
    delete_config(key="remote_repo")


@pytest.fixture
def online_mode():
    set_config(key="offline", value=False)
    yield
    set_config(key="offline", value=True)


@pytest.fixture
def offline_files():
    set_config(key="offline_files_to_add", value=[{"repo_filepath": "x", "local_filepath": "y", "remote": "z"}])


@pytest.fixture
def fake_pat():
    os.environ["qlm_token"] = "t0k3n4thewin"
    yield
    os.environ.pop("qlm_token")


@coroutine
async def fake_coroutine():
    pass


@pytest.fixture
def mock_add_files(mocker):
    mocked = mocker.patch("qlm.commands._add.add_files_to_github")
    mocked.return_value = fake_coroutine()


@pytest.fixture
def mock_delete_file(mocker):
    mocker.patch("qlm.commands._remove.delete_file")


@pytest.fixture
def mock_publish_files(mocker):
    mocked = mocker.patch("qlm.commands._publish.add_files_to_github")
    mocked.return_value = fake_coroutine()


@pytest.fixture
def mock_check_github_connection(mocker):
    yield mocker.patch("qlm.commands._connect.check_github_connection")


@pytest.fixture
def mock_download_github_repository(mocker):
    yield mocker.patch("qlm.commands._download.download_github_repository")


@pytest.fixture
def mock_call_to_editor(mocker):
    yield mocker.patch("qlm.commands._edit.os.system")


@pytest.fixture
def mock_add_files_after_editing(mocker):
    mocked = mocker.patch("qlm.commands._edit.add_files_to_github")
    mocked.return_value = fake_coroutine()
    yield mocked


@pytest.fixture
def mock_download_file_for_edit(mocker):
    yield mocker.patch("qlm.commands._edit.download_file")


@pytest.fixture
def mock_download_file_for_show(mocker):
    yield mocker.patch("qlm.commands._show.download_file")


@pytest.fixture
def mock_repo_creation(mocker):
    mocked = mocker.patch("qlm.commands._create.create_new_repo")
    mocked.return_value = "codevarna"


@pytest.fixture
def mock_get_files(mocker):
    yield mocker.patch("qlm.commands._list.get_files_in_github_repo")
