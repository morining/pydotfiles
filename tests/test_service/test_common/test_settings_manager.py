# General imports
from pathlib import Path
from _pytest.monkeypatch import MonkeyPatch
from json import dumps as json_dumps
from json import loads as json_loads
from json import load as json_load

# Project imports
from pydotfiles.service.common import SettingsManager
from pydotfiles.service.common import DEFAULT_PYDOTFILES_CACHE_DIRECTORY
from pydotfiles.service.common import DEFAULT_PYDOTFILES_LOCAL_DIRECTORY
from pydotfiles.service.common import DEFAULT_PYDOTFILES_REMOTE_REPO


"""
Cache path tests
"""


def test_settings_manager_get_cache_path_with_default(monkeypatch: MonkeyPatch):
    # Setup
    monkeypatch.delenv("PYDOTFILES_CACHE_DIRECTORY", raising=False)

    # System under test
    cache_path = SettingsManager.get_cache_path()

    # Verification
    assert DEFAULT_PYDOTFILES_CACHE_DIRECTORY == cache_path


def test_settings_manager_get_cache_path_with_env_variable_override(monkeypatch: MonkeyPatch):
    # Setup
    monkeypatch.setenv("PYDOTFILES_CACHE_DIRECTORY", "/some/other/path")

    # System under test
    cache_path = SettingsManager.get_cache_path()

    # Verification
    assert Path("/some/other/path") == cache_path


"""
Local directory tests
"""


def test_settings_manager_get_local_directory_with_default(monkeypatch: MonkeyPatch, tmp_path: Path):
    # Setup
    monkeypatch.setenv("PYDOTFILES_CACHE_DIRECTORY", str(tmp_path))
    monkeypatch.delenv("PYDOTFILES_LOCAL_DIRECTORY", raising=False)

    # System under test
    local_directory = SettingsManager.get_local_directory()

    # Verification
    assert DEFAULT_PYDOTFILES_LOCAL_DIRECTORY == local_directory


def test_settings_manager_get_local_directory_with_env_variable_override(monkeypatch: MonkeyPatch, tmp_path: Path):
    # Setup
    monkeypatch.setenv("PYDOTFILES_CACHE_DIRECTORY", str(tmp_path))
    correct_local_directory_path = tmp_path.joinpath("local")
    monkeypatch.setenv("PYDOTFILES_LOCAL_DIRECTORY", str(correct_local_directory_path))

    # System under test
    local_directory = SettingsManager.get_local_directory()

    # Verification
    assert correct_local_directory_path == local_directory


def test_settings_manager_get_local_directory_with_cache_only(monkeypatch: MonkeyPatch, tmp_path: Path):
    # Setup
    monkeypatch.setenv("PYDOTFILES_CACHE_DIRECTORY", str(tmp_path))
    test_config_file = tmp_path.joinpath("config.json")
    config_data = {
        "local_directory": "/some/other/path"
    }
    test_config_file.write_text(json_dumps(config_data))

    # System under test
    local_directory = SettingsManager.get_local_directory()

    # Verification
    assert Path("/some/other/path") == local_directory


def test_settings_manager_get_local_directory_with_cache_override(monkeypatch: MonkeyPatch, tmp_path: Path):
    # Setup
    monkeypatch.setenv("PYDOTFILES_CACHE_DIRECTORY", str(tmp_path))
    wrong_local_directory_path = tmp_path.joinpath("local")
    monkeypatch.setenv("PYDOTFILES_LOCAL_DIRECTORY", str(wrong_local_directory_path))
    test_config_file = tmp_path.joinpath("config.json")
    config_data = {
        "local_directory": "/some/correct/path"
    }
    test_config_file.write_text(json_dumps(config_data))

    # System under test
    local_directory = SettingsManager.get_local_directory()

    # Verification
    assert Path("/some/correct/path") == local_directory


def test_settings_manager_set_local_directory_with_no_initial_directory(monkeypatch: MonkeyPatch, tmp_path: Path):
    # Setup
    cache_subdirectory = tmp_path.joinpath("cache")
    monkeypatch.setenv("PYDOTFILES_CACHE_DIRECTORY", str(cache_subdirectory))
    correct_local_directory = tmp_path.joinpath("local")
    test_config_file = cache_subdirectory.joinpath("config.json")

    # System under test
    SettingsManager.set_local_directory(correct_local_directory)

    # Verification
    new_local_directory = SettingsManager.get_local_directory()
    assert cache_subdirectory.is_dir()
    assert test_config_file.is_file()
    with test_config_file.open("r") as test_config_fp:
        final_test_config_data = json_loads(test_config_fp.read())
    assert correct_local_directory == Path(final_test_config_data.get("local_directory"))
    assert final_test_config_data.get("remote_repo") is None
    assert correct_local_directory == new_local_directory


def test_settings_manager_set_local_directory_with_empty_initial_directory(monkeypatch: MonkeyPatch, tmp_path: Path):
    # Setup
    cache_subdirectory = tmp_path.joinpath("cache")
    cache_subdirectory.mkdir()
    monkeypatch.setenv("PYDOTFILES_CACHE_DIRECTORY", str(cache_subdirectory))
    correct_local_directory = tmp_path.joinpath("local")
    test_config_file = cache_subdirectory.joinpath("config.json")

    # System under test
    SettingsManager.set_local_directory(correct_local_directory)

    # Verification
    new_local_directory = SettingsManager.get_local_directory()
    assert test_config_file.is_file()
    with test_config_file.open("r") as test_config_fp:
        final_test_config_data = json_loads(test_config_fp.read())
    assert correct_local_directory == Path(final_test_config_data.get("local_directory"))
    assert final_test_config_data.get("remote_repo") is None
    assert correct_local_directory == new_local_directory


def test_settings_manager_set_local_directory_with_existing_local_directory(monkeypatch: MonkeyPatch, tmp_path: Path):
    # Setup
    cache_subdirectory = tmp_path.joinpath("cache")
    cache_subdirectory.mkdir()
    monkeypatch.setenv("PYDOTFILES_CACHE_DIRECTORY", str(cache_subdirectory))
    correct_local_directory = tmp_path.joinpath("local")
    test_config_file = cache_subdirectory.joinpath("config.json")
    test_config_data = {
        "local_directory": "/some/directory/containing/the/old/local/dotfiles"
    }
    test_config_file.write_text(json_dumps(test_config_data))

    # System under test
    SettingsManager.set_local_directory(correct_local_directory)

    # Verification
    new_local_directory = SettingsManager.get_local_directory()
    assert test_config_file.is_file()
    with test_config_file.open("r") as test_config_fp:
        final_test_config_data = json_loads(test_config_fp.read())

    assert correct_local_directory == Path(final_test_config_data.get("local_directory"))
    assert final_test_config_data.get("remote_repo") is None
    assert correct_local_directory == new_local_directory


def test_settings_manager_set_local_directory_with_existing_remote_repo(monkeypatch: MonkeyPatch, tmp_path: Path):
    # Setup
    cache_subdirectory = tmp_path.joinpath("cache")
    cache_subdirectory.mkdir()
    monkeypatch.setenv("PYDOTFILES_CACHE_DIRECTORY", str(cache_subdirectory))
    correct_local_directory = tmp_path.joinpath("local")
    test_config_file = cache_subdirectory.joinpath("config.json")
    test_config_data = {
        "remote_repo": "https://github.com/some/link-to-your-remote-repo.git"
    }
    test_config_file.write_text(json_dumps(test_config_data))

    # System under test
    SettingsManager.set_local_directory(correct_local_directory)

    # Verification
    new_local_directory = SettingsManager.get_local_directory()
    assert test_config_file.is_file()
    with test_config_file.open("r") as test_config_fp:
        final_test_config_data = json_loads(test_config_fp.read())

    assert correct_local_directory == Path(final_test_config_data.get("local_directory"))
    assert "https://github.com/some/link-to-your-remote-repo.git" == final_test_config_data.get("remote_repo")
    assert correct_local_directory == new_local_directory


def test_settings_manager_set_local_directory_with_all_existing_data(monkeypatch: MonkeyPatch, tmp_path: Path):
    # Setup
    cache_subdirectory = tmp_path.joinpath("cache")
    cache_subdirectory.mkdir()
    monkeypatch.setenv("PYDOTFILES_CACHE_DIRECTORY", str(cache_subdirectory))
    correct_local_directory = tmp_path.joinpath("local")
    test_config_file = cache_subdirectory.joinpath("config.json")
    test_config_data = {
        "remote_repo": "https://github.com/some/link-to-your-remote-repo.git",
        "local_directory": "/some/directory/containing/the/old/local/dotfiles"
    }
    test_config_file.write_text(json_dumps(test_config_data))

    # System under test
    SettingsManager.set_local_directory(correct_local_directory)

    # Verification
    new_local_directory = SettingsManager.get_local_directory()
    assert test_config_file.is_file()
    with test_config_file.open("r") as test_config_fp:
        final_test_config_data = json_loads(test_config_fp.read())

    assert correct_local_directory == Path(final_test_config_data.get("local_directory"))
    assert "https://github.com/some/link-to-your-remote-repo.git" == final_test_config_data.get("remote_repo")
    assert correct_local_directory == new_local_directory


"""
Remote repo tests
"""


def test_settings_manager_get_remote_repo_with_default(monkeypatch: MonkeyPatch, tmp_path: Path):
    # Setup
    monkeypatch.setenv("PYDOTFILES_CACHE_DIRECTORY", str(tmp_path))
    monkeypatch.delenv("PYDOTFILES_REMOTE_REPO", raising=False)

    # System under test
    remote_repo = SettingsManager.get_remote_repo()

    # Verification
    assert DEFAULT_PYDOTFILES_REMOTE_REPO == remote_repo


def test_settings_manager_get_remote_repo_with_env_variable_override(monkeypatch: MonkeyPatch, tmp_path: Path):
    # Setup
    monkeypatch.setenv("PYDOTFILES_CACHE_DIRECTORY", str(tmp_path))
    monkeypatch.setenv("PYDOTFILES_REMOTE_REPO", "https://github.com/some/link-to-your-remote-repo.git")

    # System under test
    remote_repo = SettingsManager.get_remote_repo()

    # Verification
    assert "https://github.com/some/link-to-your-remote-repo.git" == remote_repo


def test_settings_manager_get_remote_repo_with_cache_only(monkeypatch: MonkeyPatch, tmp_path: Path):
    # Setup
    monkeypatch.setenv("PYDOTFILES_CACHE_DIRECTORY", str(tmp_path))
    test_config_file = tmp_path.joinpath("config.json")
    config_data = {
        "remote_repo": "https://github.com/some/link-to-your-remote-repo.git"
    }
    test_config_file.write_text(json_dumps(config_data))

    # System under test
    remote_repo = SettingsManager.get_remote_repo()

    # Verification
    assert "https://github.com/some/link-to-your-remote-repo.git" == remote_repo


def test_settings_manager_get_remote_repo_with_cache_override(monkeypatch: MonkeyPatch, tmp_path: Path):
    # Setup
    monkeypatch.setenv("PYDOTFILES_CACHE_DIRECTORY", str(tmp_path))
    monkeypatch.setenv("PYDOTFILES_REMOTE_REPO", "https://github.com/some/wrong-link-to-your-remote-repo.git")
    test_config_file = tmp_path.joinpath("config.json")
    config_data = {
        "remote_repo": "https://github.com/some/correct-link-to-your-remote-repo.git"
    }
    test_config_file.write_text(json_dumps(config_data))

    # System under test
    remote_repo = SettingsManager.get_remote_repo()

    # Verification
    assert "https://github.com/some/correct-link-to-your-remote-repo.git" == remote_repo


def test_settings_manager_set_remote_repo_with_no_initial_directory(monkeypatch: MonkeyPatch, tmp_path: Path):
    # Setup
    cache_subdirectory = tmp_path.joinpath("cache")
    monkeypatch.setenv("PYDOTFILES_CACHE_DIRECTORY", str(cache_subdirectory))
    correct_remote_repo = "https://github.com/some/correct-link-to-your-remote-repo.git"
    test_config_file = cache_subdirectory.joinpath("config.json")

    # System under test
    SettingsManager.set_remote_repo(correct_remote_repo)

    # Verification
    new_remote_repo = SettingsManager.get_remote_repo()
    assert cache_subdirectory.is_dir()
    assert test_config_file.is_file()
    with test_config_file.open("r") as test_config_fp:
        final_test_config_data = json_load(test_config_fp)
    assert correct_remote_repo == final_test_config_data.get("remote_repo")
    assert final_test_config_data.get("local_directory") is None
    assert correct_remote_repo == new_remote_repo


def test_settings_manager_set_remote_repo_with_empty_initial_directory(monkeypatch: MonkeyPatch, tmp_path: Path):
    # Setup
    cache_subdirectory = tmp_path.joinpath("cache")
    cache_subdirectory.mkdir()
    monkeypatch.setenv("PYDOTFILES_CACHE_DIRECTORY", str(cache_subdirectory))
    correct_remote_repo = "https://github.com/some/correct-link-to-your-remote-repo.git"
    test_config_file = cache_subdirectory.joinpath("config.json")

    # System under test
    SettingsManager.set_remote_repo(correct_remote_repo)

    # Verification
    new_remote_repo = SettingsManager.get_remote_repo()
    assert test_config_file.is_file()
    with test_config_file.open("r") as test_config_fp:
        final_test_config_data = json_load(test_config_fp)
    assert correct_remote_repo == final_test_config_data.get("remote_repo")
    assert final_test_config_data.get("local_directory") is None
    assert correct_remote_repo == new_remote_repo


def test_settings_manager_set_remote_repo_with_existing_local_directory(monkeypatch: MonkeyPatch, tmp_path: Path):
    # Setup
    cache_subdirectory = tmp_path.joinpath("cache")
    cache_subdirectory.mkdir()
    monkeypatch.setenv("PYDOTFILES_CACHE_DIRECTORY", str(cache_subdirectory))
    correct_remote_repo = "https://github.com/some/correct-link-to-your-remote-repo.git"
    test_config_file = cache_subdirectory.joinpath("config.json")
    test_config_data = {
        "local_directory": "/some/directory/containing/the/existing/local/dotfiles"
    }
    test_config_file.write_text(json_dumps(test_config_data))

    # System under test
    SettingsManager.set_remote_repo(correct_remote_repo)

    # Verification
    new_remote_repo = SettingsManager.get_remote_repo()
    assert test_config_file.is_file()
    with test_config_file.open("r") as test_config_fp:
        final_test_config_data = json_load(test_config_fp)
    assert correct_remote_repo == final_test_config_data.get("remote_repo")
    assert "/some/directory/containing/the/existing/local/dotfiles" == final_test_config_data.get("local_directory")
    assert correct_remote_repo == new_remote_repo


def test_settings_manager_set_remote_repo_with_existing_remote_repo(monkeypatch: MonkeyPatch, tmp_path: Path):
    # Setup
    cache_subdirectory = tmp_path.joinpath("cache")
    cache_subdirectory.mkdir()
    monkeypatch.setenv("PYDOTFILES_CACHE_DIRECTORY", str(cache_subdirectory))
    correct_remote_repo = "https://github.com/some/correct-link-to-your-remote-repo.git"
    test_config_file = cache_subdirectory.joinpath("config.json")
    test_config_data = {
        "remote_repo": "https://github.com/some/link-to-your-old-remote-repo.git"
    }
    test_config_file.write_text(json_dumps(test_config_data))

    # System under test
    SettingsManager.set_remote_repo(correct_remote_repo)

    # Verification
    new_remote_repo = SettingsManager.get_remote_repo()
    assert test_config_file.is_file()
    with test_config_file.open("r") as test_config_fp:
        final_test_config_data = json_load(test_config_fp)
    assert correct_remote_repo == final_test_config_data.get("remote_repo")
    assert final_test_config_data.get("local_directory") is None
    assert correct_remote_repo == new_remote_repo


def test_settings_manager_set_remote_repo_with_all_existing_data(monkeypatch: MonkeyPatch, tmp_path: Path):
    # Setup
    cache_subdirectory = tmp_path.joinpath("cache")
    cache_subdirectory.mkdir()
    monkeypatch.setenv("PYDOTFILES_CACHE_DIRECTORY", str(cache_subdirectory))
    correct_remote_repo = "https://github.com/some/correct-link-to-your-remote-repo.git"
    test_config_file = cache_subdirectory.joinpath("config.json")
    test_config_data = {
        "remote_repo": "https://github.com/some/link-to-your-old-remote-repo.git",
        "local_directory": "/some/directory/containing/the/old/local/dotfiles"
    }
    test_config_file.write_text(json_dumps(test_config_data))

    # System under test
    SettingsManager.set_remote_repo(correct_remote_repo)

    # Verification
    new_remote_repo = SettingsManager.get_remote_repo()
    assert test_config_file.is_file()
    with test_config_file.open("r") as test_config_fp:
        final_test_config_data = json_load(test_config_fp)
    assert correct_remote_repo == final_test_config_data.get("remote_repo")
    assert "/some/directory/containing/the/old/local/dotfiles" == final_test_config_data.get("local_directory")
    assert correct_remote_repo == new_remote_repo
