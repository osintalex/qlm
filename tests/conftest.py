import os
from tempfile import TemporaryDirectory
from asyncio import coroutine

import pytest
from typer.testing import CliRunner

from tools.config_helpers import set_config, delete_config


@pytest.fixture
def runner():
    yield CliRunner()


@pytest.fixture
def local_repo():
    tmpdir = TemporaryDirectory()
    set_config(key="local_repo", value=tmpdir.name)
    yield
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


@pytest.fixture()
def online_mode():
    set_config(key="offline", value=False)
    yield
    set_config(key="offline", value=True)


@pytest.fixture()
def fake_pat():
    os.environ["qlm_token"] = "t0k3n4thewin"
    yield
    os.environ.pop("qlm_token")


@coroutine
async def fake_coroutine():
    pass


@pytest.fixture()
def mock_add_files(mocker):
    mocked = mocker.patch("commands._add.add_files_to_github")
    mocked.return_value = fake_coroutine()
