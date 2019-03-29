# General imports
from pathlib import Path
from configparser import ConfigParser
from os import walk

# Vendor imports
from _pytest.monkeypatch import MonkeyPatch
from pytest import mark
from git import Repo

# Project imports
from pydotfiles.service.update import UpdateHandler
from pydotfiles.service.common import DEFAULT_PYDOTFILES_REMOTE_REPO
from pydotfiles.service.common import ResponseCode


@mark.integration
def test_successful_update_when_already_latest(baseline_local_repo, tmp_path: Path):
    # Setup
    request = {}

    # System under test
    response = UpdateHandler.update(request)

    # Verification
    assert response.is_ok
    assert "Update: Successfully updated local dotfiles repo with the latest remote changes" == response.response_message


@mark.integration
def test_successful_update_when_3_commits_from_remote_head(older_local_repo, tmp_path: Path, monkeypatch: MonkeyPatch):
    # Setup
    request = {}
    local_directory_path = tmp_path.joinpath("local")
    repo = Repo(local_directory_path)
    old_commit_sha = str(repo.head.object.hexsha)

    # System under test
    response = UpdateHandler.update(request)

    # Verification
    assert response.is_ok
    assert "Update: Successfully updated local dotfiles repo with the latest remote changes" == response.response_message
    assert local_directory_path.is_dir()

    git_directory = local_directory_path.joinpath(".git")
    assert git_directory.is_dir()
    parser = ConfigParser()
    parser.read(git_directory.joinpath("config"))
    assert DEFAULT_PYDOTFILES_REMOTE_REPO == parser["remote \"origin\""]["url"]
    new_commit_sha = str(repo.head.object.hexsha)
    assert old_commit_sha != new_commit_sha

    fetch_head_path = git_directory.joinpath("FETCH_HEAD")
    identified_current_head = fetch_head_path.read_text().split()[0]
    assert identified_current_head == new_commit_sha


@mark.integration
def test_fail_update_when_3_commits_from_remote_head_and_dirty_context(older_local_repo, tmp_path: Path, monkeypatch: MonkeyPatch):
    # Setup
    request = {}
    local_directory_path = tmp_path.joinpath("local")
    repo = Repo(local_directory_path)
    old_commit_sha = str(repo.head.object.hexsha)
    replace_all_files_in_path_with_text(local_directory_path)

    # System under test
    response = UpdateHandler.update(request)

    # Verification
    assert not response.is_ok
    assert "Update: Failed to update local dotfiles repo with the latest remote changes" == response.response_message
    assert response.response_code == ResponseCode.LOCAL_CHANGES_TO_GIT_REPO_PREVENTING_UPDATE

    git_directory = local_directory_path.joinpath(".git")
    assert git_directory.is_dir()
    parser = ConfigParser()
    parser.read(git_directory.joinpath("config"))
    assert DEFAULT_PYDOTFILES_REMOTE_REPO == parser["remote \"origin\""]["url"]
    new_commit_sha = str(repo.head.object.hexsha)
    assert old_commit_sha == new_commit_sha

    fetch_head_path = git_directory.joinpath("FETCH_HEAD")
    identified_current_head = fetch_head_path.read_text().split()[0]
    assert identified_current_head != new_commit_sha


def replace_all_files_in_path_with_text(path: Path):
    for path_prefix, directory_names, file_names in walk(path):
        directory_names[:] = [directory_name for directory_name in directory_names if directory_name != ".git"]
        for file_name in file_names:
            if file_name.startswith(".git"):
                continue
            file_name_path = Path(path_prefix).joinpath(file_name)
            Path(file_name_path).write_text("some random text\n")
