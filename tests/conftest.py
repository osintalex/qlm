import pytest
import os

from typer.testing import CliRunner
from tempfile import TemporaryDirectory

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
