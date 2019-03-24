# General imports
from argparse import Namespace
from pathlib import Path
from _pytest.monkeypatch import MonkeyPatch

# Project imports
from pydotfiles.service.clean import CleanHandler
from pydotfiles.service.common import ResponseCode


"""
Cache cleaning tests
"""


def test_successful_clean_cache_with_no_existing_directory(monkeypatch: MonkeyPatch, tmp_path: Path):
    # Setup
    cache_directory_path = tmp_path.joinpath("cache")
    monkeypatch.setenv("PYDOTFILES_CACHE_DIRECTORY", str(cache_directory_path))
    request = Namespace()
    request.clean_target = "cache"

    # System under test
    response = CleanHandler.clean(request)

    # Verification
    assert response.is_ok
    assert response.response_message.startswith("Clean: The directory has already been cleaned")
    assert not cache_directory_path.is_dir()


def test_successful_clean_cache_with_existing_empty_directory(monkeypatch: MonkeyPatch, tmp_path: Path):
    # Setup
    cache_directory_path = tmp_path.joinpath("cache")
    cache_directory_path.mkdir()
    monkeypatch.setenv("PYDOTFILES_CACHE_DIRECTORY", str(cache_directory_path))
    request = Namespace()
    request.clean_target = "cache"

    # System under test
    response = CleanHandler.clean(request)

    # Verification
    assert response.is_ok
    assert response.response_message.startswith("Clean: Successfully cleaned out the directory")
    assert not cache_directory_path.is_dir()


def test_successful_clean_cache_with_existing_directory_and_file(monkeypatch: MonkeyPatch, tmp_path: Path):
    # Setup
    cache_directory_path = tmp_path.joinpath("cache")
    cache_directory_path.mkdir()
    fake_file_a = cache_directory_path.joinpath("a.file")
    fake_file_a.write_text("example")
    monkeypatch.setenv("PYDOTFILES_CACHE_DIRECTORY", str(cache_directory_path))
    request = Namespace()
    request.clean_target = "cache"

    # System under test
    response = CleanHandler.clean(request)

    # Verification
    assert response.is_ok
    assert response.response_message.startswith("Clean: Successfully cleaned out the directory")
    assert not fake_file_a.is_file()
    assert not cache_directory_path.is_dir()


def test_failed_clean_cache_with_directory_removal_failure(monkeypatch: MonkeyPatch, tmp_path: Path):
    # Setup
    cache_directory_path = tmp_path.joinpath("cache")
    cache_directory_path.mkdir()
    monkeypatch.setenv("PYDOTFILES_CACHE_DIRECTORY", str(cache_directory_path))

    def mock_throw_exception(clean_target: Path):
        raise OSError("Cannot call rmtree on a symbolic link")

    monkeypatch.setattr(CleanHandler, 'clean_target', mock_throw_exception)

    request = Namespace()
    request.clean_target = "cache"

    # System under test
    response = CleanHandler.clean(request)

    # Verification
    assert ResponseCode.UNKNOWN_CLEANING_ERROR == response.response_code
    assert "Cannot call rmtree on a symbolic link" == response.response_message
    assert cache_directory_path.is_dir()


"""
Repo cleaning tests
"""


def test_successful_clean_repo_with_no_existing_directory(monkeypatch: MonkeyPatch, tmp_path: Path):
    # Setup
    local_repo_path = tmp_path.joinpath("local")
    monkeypatch.setenv("PYDOTFILES_LOCAL_DIRECTORY", str(local_repo_path))
    request = Namespace()
    request.clean_target = "repo"

    # System under test
    response = CleanHandler.clean(request)

    # Verification
    assert response.is_ok
    assert response.response_message.startswith("Clean: The directory has already been cleaned")
    assert not local_repo_path.is_dir()


def test_successful_clean_repo_with_existing_empty_directory(monkeypatch: MonkeyPatch, tmp_path: Path):
    # Setup
    local_repo_path = tmp_path.joinpath("local")
    local_repo_path.mkdir()
    monkeypatch.setenv("PYDOTFILES_LOCAL_DIRECTORY", str(local_repo_path))
    request = Namespace()
    request.clean_target = "repo"

    # System under test
    response = CleanHandler.clean(request)

    # Verification
    assert response.is_ok
    assert response.response_message.startswith("Clean: Successfully cleaned out the directory")
    assert not local_repo_path.is_dir()


def test_successful_clean_repo_with_existing_directory_and_file(monkeypatch: MonkeyPatch, tmp_path: Path):
    # Setup
    local_repo_path = tmp_path.joinpath("local")
    local_repo_path.mkdir()
    fake_file_a = local_repo_path.joinpath("a.file")
    fake_file_a.write_text("example")
    monkeypatch.setenv("PYDOTFILES_LOCAL_DIRECTORY", str(local_repo_path))
    request = Namespace()
    request.clean_target = "repo"

    # System under test
    response = CleanHandler.clean(request)

    # Verification
    assert response.is_ok
    assert response.response_message.startswith("Clean: Successfully cleaned out the directory")
    assert not local_repo_path.is_dir()
    assert not fake_file_a.is_file()


def test_failed_clean_repo_with_directory_removal_failure(monkeypatch: MonkeyPatch, tmp_path: Path):
    # Setup
    local_repo_path = tmp_path.joinpath("local")
    local_repo_path.mkdir()
    monkeypatch.setenv("PYDOTFILES_LOCAL_DIRECTORY", str(local_repo_path))

    def mock_throw_exception(clean_target: Path):
        raise OSError("Failed because Cthulu looked at this code weirdly")
    monkeypatch.setattr(CleanHandler, 'clean_target', mock_throw_exception)

    request = Namespace()
    request.clean_target = "repo"

    # System under test
    response = CleanHandler.clean(request)

    # Verification
    assert ResponseCode.UNKNOWN_CLEANING_ERROR == response.response_code
    assert "Failed because Cthulu looked at this code weirdly" == response.response_message
    assert local_repo_path.is_dir()
