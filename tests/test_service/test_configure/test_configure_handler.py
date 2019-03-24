# General imports
from pathlib import Path
from _pytest.monkeypatch import MonkeyPatch
from json import load as json_load

# Project imports
from pydotfiles.service.configure import ConfigureHandler


def test_successful_configure_with_no_arguments(monkeypatch: MonkeyPatch, tmp_path: Path):
    # Setup
    cache_directory_path = tmp_path.joinpath("cache")
    monkeypatch.setenv("PYDOTFILES_CACHE_DIRECTORY", str(cache_directory_path))

    local_directory_path = tmp_path.joinpath("local")
    monkeypatch.setenv("PYDOTFILES_LOCAL_DIRECTORY", str(local_directory_path))

    request = {}

    # System under test
    response = ConfigureHandler.configure(request)

    # Verification
    assert response.is_ok
    assert response.response_message.startswith("Configure: No configuration setting passed in")
    assert not local_directory_path.is_dir()


def test_successful_configure_with_local_directory(monkeypatch: MonkeyPatch, tmp_path: Path):
    # Setup
    cache_directory_path = tmp_path.joinpath("cache")
    monkeypatch.setenv("PYDOTFILES_CACHE_DIRECTORY", str(cache_directory_path))

    old_local_directory_path = tmp_path.joinpath("old-local")
    monkeypatch.setenv("PYDOTFILES_LOCAL_DIRECTORY", str(old_local_directory_path))

    new_local_directory_path = tmp_path.joinpath("new-local")
    request = {
        "local_directory": str(new_local_directory_path)
    }

    # System under test
    response = ConfigureHandler.configure(request)

    # Verification
    config_file_path = cache_directory_path.joinpath("config.json")
    assert response.is_ok
    assert response.response_message.startswith("Configure: Successfully persisted configuration data")
    assert cache_directory_path.is_dir()
    assert config_file_path.is_file()
    with config_file_path.open("r") as config_fp:
        persisted_config_data = json_load(config_fp)

    assert str(new_local_directory_path) == persisted_config_data.get("local_directory")
    assert persisted_config_data.get("remote_repo") is None


def test_successful_configure_with_remote_repo(monkeypatch: MonkeyPatch, tmp_path: Path):
    # Setup
    cache_directory_path = tmp_path.joinpath("cache")
    monkeypatch.setenv("PYDOTFILES_CACHE_DIRECTORY", str(cache_directory_path))

    local_directory_path = tmp_path.joinpath("local")
    monkeypatch.setenv("PYDOTFILES_LOCAL_DIRECTORY", str(local_directory_path))

    request = {
        "remote_repo": "https://github.com/some/new-repo.git"
    }

    # System under test
    response = ConfigureHandler.configure(request)

    # Verification
    config_file_path = cache_directory_path.joinpath("config.json")
    assert response.is_ok
    assert response.response_message.startswith("Configure: Successfully persisted configuration data")
    assert cache_directory_path.is_dir()
    assert config_file_path.is_file()
    with config_file_path.open("r") as config_fp:
        persisted_config_data = json_load(config_fp)

    assert "https://github.com/some/new-repo.git" == persisted_config_data.get("remote_repo")
    assert persisted_config_data.get("local_directory") is None
