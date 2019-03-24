# General imports
from pathlib import Path
from configparser import ConfigParser

# Vendor imports
from _pytest.monkeypatch import MonkeyPatch
from pytest import mark

# Project imports
from pydotfiles.service.download import DownloadHandler
from pydotfiles.service.common import DEFAULT_PYDOTFILES_REMOTE_REPO


"""
Baseline tests
"""


@mark.integration
def test_successful_download_with_no_arguments(monkeypatch: MonkeyPatch, tmp_path: Path):
    # Setup
    local_directory_path = tmp_path.joinpath("local")
    monkeypatch.setenv("PYDOTFILES_LOCAL_DIRECTORY", str(local_directory_path))
    monkeypatch.setenv("PYDOTFILES_CACHE_DIRECTORY", str(tmp_path))
    monkeypatch.delenv("PYDOTFILES_REMOTE_REPO", raising=False)

    request = {}

    # System under test
    response = DownloadHandler.download(request)

    # Verification
    assert response.is_ok
    assert "Download: Successfully cloned git repository" == response.response_message
    assert local_directory_path.is_dir()

    git_directory = local_directory_path.joinpath(".git")
    assert git_directory.is_dir()
    parser = ConfigParser()
    parser.read(git_directory.joinpath("config"))
    assert DEFAULT_PYDOTFILES_REMOTE_REPO == parser["remote \"origin\""]["url"]


"""
Request only tests
"""


@mark.integration
def test_successful_download_with_local_directory_request_only(monkeypatch: MonkeyPatch, tmp_path: Path):
    # Setup
    old_local_directory_path = tmp_path.joinpath("old-local")
    new_local_directory_path = tmp_path.joinpath("new-local")
    monkeypatch.setenv("PYDOTFILES_LOCAL_DIRECTORY", str(old_local_directory_path))
    monkeypatch.setenv("PYDOTFILES_CACHE_DIRECTORY", str(tmp_path))
    monkeypatch.delenv("PYDOTFILES_REMOTE_REPO", raising=False)

    request = {
        "local_directory": str(new_local_directory_path)
    }

    # System under test
    response = DownloadHandler.download(request)

    # Verification
    assert response.is_ok
    assert "Download: Successfully cloned git repository" == response.response_message
    assert not old_local_directory_path.is_dir()
    assert new_local_directory_path.is_dir()

    git_directory = new_local_directory_path.joinpath(".git")
    assert git_directory.is_dir()
    parser = ConfigParser()
    parser.read(git_directory.joinpath("config"))
    assert DEFAULT_PYDOTFILES_REMOTE_REPO == parser["remote \"origin\""]["url"]


@mark.integration
def test_successful_download_with_valid_remote_repo_request_only(monkeypatch: MonkeyPatch, tmp_path: Path):
    # Setup
    local_directory_path = tmp_path.joinpath("local")
    monkeypatch.setenv("PYDOTFILES_LOCAL_DIRECTORY", str(local_directory_path))
    monkeypatch.setenv("PYDOTFILES_CACHE_DIRECTORY", str(tmp_path))
    monkeypatch.delenv("PYDOTFILES_REMOTE_REPO", raising=False)

    request = {
        "remote_repo": "git@github.com:JasonYao/dotfiles.git"
    }

    # System under test
    response = DownloadHandler.download(request)

    # Verification
    assert response.is_ok
    assert "Download: Successfully cloned git repository" == response.response_message
    assert local_directory_path.is_dir()

    git_directory = local_directory_path.joinpath(".git")
    assert git_directory.is_dir()
    parser = ConfigParser()
    parser.read(git_directory.joinpath("config"))
    assert "git@github.com:JasonYao/dotfiles.git" == parser["remote \"origin\""]["url"]


@mark.integration
def test_failed_download_with_invalid_remote_repo_request_only(monkeypatch: MonkeyPatch, tmp_path: Path):
    # Setup
    local_directory_path = tmp_path.joinpath("local")
    monkeypatch.setenv("PYDOTFILES_LOCAL_DIRECTORY", str(local_directory_path))
    monkeypatch.setenv("PYDOTFILES_CACHE_DIRECTORY", str(tmp_path))
    monkeypatch.delenv("PYDOTFILES_REMOTE_REPO", raising=False)

    request = {
        "remote_repo": "git@github.com:JasonYao/invalid-url.git"
    }

    # System under test
    response = DownloadHandler.download(request)

    # Verification
    assert not response.is_ok
    assert "Download: Failed to clone git repository" == response.response_message
    assert not local_directory_path.is_dir()


@mark.integration
def test_successful_download_with_local_directory_and_remote_repo_request(monkeypatch: MonkeyPatch, tmp_path: Path):
    # Setup
    old_local_directory_path = tmp_path.joinpath("old-local")
    new_local_directory_path = tmp_path.joinpath("new-local")
    monkeypatch.setenv("PYDOTFILES_LOCAL_DIRECTORY", str(old_local_directory_path))
    monkeypatch.setenv("PYDOTFILES_CACHE_DIRECTORY", str(tmp_path))
    monkeypatch.delenv("PYDOTFILES_REMOTE_REPO", raising=False)

    request = {
        "local_directory": str(new_local_directory_path),
        "remote_repo": "git@github.com:JasonYao/dotfiles.git"
    }

    # System under test
    response = DownloadHandler.download(request)

    # Verification
    assert response.is_ok
    assert "Download: Successfully cloned git repository" == response.response_message
    assert not old_local_directory_path.is_dir()
    assert new_local_directory_path.is_dir()

    git_directory = new_local_directory_path.joinpath(".git")
    assert git_directory.is_dir()
    parser = ConfigParser()
    parser.read(git_directory.joinpath("config"))
    assert "git@github.com:JasonYao/dotfiles.git" == parser["remote \"origin\""]["url"]
