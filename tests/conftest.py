# General imports
from typing import List
from pathlib import Path
from configparser import ConfigParser

# Vendor imports
from pytest import mark
from pytest import fixture
from _pytest.config import Config
from _pytest.monkeypatch import MonkeyPatch
from git import Repo

# Project imports
from pydotfiles.service.download import DownloadHandler
from pydotfiles.service.common import DEFAULT_PYDOTFILES_REMOTE_REPO


def pytest_addoption(parser):
    parser.addoption("--runslow", action="store_true", default=False, help="Runs slow tests")
    parser.addoption("--run-integration-tests", action="store_true", default=False, help="Runs slower integration tests that do real IO/network calls")
    parser.addoption("--run-end-to-end-tests", action="store_true", default=False, help="Runs extremely slow end-to-end tests that do real IO/network calls")


def pytest_collection_modifyitems(config: Config, items: List):
    if not config.getoption("--runslow"):
        # --runslow not given in the cli: skip slow tests
        skip_slow = mark.skip(reason="need --runslow option to run")
        for item in items:
            if "slow" in item.keywords:
                item.add_marker(skip_slow)

    if not config.getoption("--run-integration-tests"):
        # --run-integration-tests not given in the cli: skip integration tests
        skip_integration = mark.skip(reason="need --run-integration-tests option to run")
        for item in items:
            if "integration" in item.keywords:
                item.add_marker(skip_integration)

    if not config.getoption("--run-end-to-end-tests"):
        # --run-end-to-end-tests not given in the cli: skip end-to-end tests
        skip_integration = mark.skip(reason="need --run-end-to-end-tests option to run")
        for item in items:
            if "etoe" in item.keywords:
                item.add_marker(skip_integration)


@fixture
def baseline_local_repo(monkeypatch: MonkeyPatch, tmp_path: Path):
    local_directory_path = tmp_path.joinpath("local")
    monkeypatch.setenv("PYDOTFILES_LOCAL_DIRECTORY", str(local_directory_path))
    monkeypatch.setenv("PYDOTFILES_CACHE_DIRECTORY", str(tmp_path))
    monkeypatch.delenv("PYDOTFILES_REMOTE_REPO", raising=False)
    request = {}
    response = DownloadHandler.download(request)

    # Fixture verification
    assert response.is_ok
    assert "Download: Successfully cloned git repository" == response.response_message
    assert local_directory_path.is_dir()

    git_directory = local_directory_path.joinpath(".git")
    assert git_directory.is_dir()
    parser = ConfigParser()
    parser.read(git_directory.joinpath("config"))
    assert DEFAULT_PYDOTFILES_REMOTE_REPO == parser["remote \"origin\""]["url"]


@fixture
def older_local_repo(monkeypatch: MonkeyPatch, tmp_path: Path):
    local_directory_path = tmp_path.joinpath("local")
    monkeypatch.setenv("PYDOTFILES_LOCAL_DIRECTORY", str(local_directory_path))
    monkeypatch.setenv("PYDOTFILES_CACHE_DIRECTORY", str(tmp_path))
    monkeypatch.delenv("PYDOTFILES_REMOTE_REPO", raising=False)
    request = {}
    response = DownloadHandler.download(request)

    # Original fixture verification
    assert response.is_ok
    assert "Download: Successfully cloned git repository" == response.response_message
    assert local_directory_path.is_dir()

    git_directory = local_directory_path.joinpath(".git")
    assert git_directory.is_dir()
    parser = ConfigParser()
    parser.read(git_directory.joinpath("config"))
    assert DEFAULT_PYDOTFILES_REMOTE_REPO == parser["remote \"origin\""]["url"]

    # Hard resets to an older commit
    repo = Repo(local_directory_path)
    repo.git.reset('--hard', 'HEAD~3')
