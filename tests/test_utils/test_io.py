import os
import filecmp
import pytest

from pydotfiles.utils import mv_file, rm_file, copy_file, symlink_file, unsymlink_file, run_file, run_command
from pydotfiles.utils import is_moved, is_broken_link, is_linked, is_copied, is_executable


"""
Move file tests
"""


def test_mv_file_success(tmpdir):
    # Setup
    original_file = tmpdir.join("origin.somefile")
    destination_file = tmpdir.join("destination.somefile")
    original_file_content = "some content"
    original_file.write(original_file_content)

    # System under test
    mv_file(original_file, destination_file)

    # Verification
    destination_file_content = destination_file.read()

    assert original_file_content == destination_file_content
    assert not os.path.isfile(original_file)


def test_mv_file_fail_none():
    with pytest.raises(RuntimeError):
        # System under test
        mv_file(None, None)


def test_mv_file_fail_with_existing_destination_file(tmpdir):
    # Setup
    original_file = tmpdir.join("origin.somefile")
    original_file.write("")
    destination_file = tmpdir.join("destination.somefile")
    destination_file.write("some content")

    with pytest.raises(RuntimeError):
        # System under test
        mv_file(original_file, destination_file)


"""
Remove file tests
"""


def test_rm_file_success(tmpdir):
    # Setup
    original_file = tmpdir.join("origin.somefile")
    original_file_content = "some content"
    original_file.write(original_file_content)

    # System under test
    rm_file(original_file)

    # Verification
    assert not os.path.isfile(original_file)


def test_rm_file_fail_none():
    with pytest.raises(RuntimeError):
        # System under test
        rm_file(None)


"""
Copy file tests
"""


def test_copy_file_success(tmpdir):
    # Setup
    original_file = tmpdir.join("origin.somefile")
    destination_file = tmpdir.join("destination.somefile")
    original_file_content = "some content"
    original_file.write(original_file_content)

    # System under test
    copy_file(original_file, destination_file)

    # Verification
    destination_file_content = destination_file.read()

    assert original_file_content == destination_file_content
    assert filecmp.cmp(original_file, destination_file)


def test_copy_file_fail_none():
    with pytest.raises(RuntimeError):
        # System under test
        copy_file(None, None)


def test_copy_file_fail_with_existing_destination_file(tmpdir):
    # Setup
    original_file = tmpdir.join("origin.somefile")
    original_file.write("")
    destination_file = tmpdir.join("destination.somefile")
    destination_file.write("some content")

    with pytest.raises(RuntimeError):
        # System under test
        copy_file(original_file, destination_file)


"""
Symlink file tests
"""


def test_symlink_file_success(tmpdir):
    # Setup
    original_file = tmpdir.join("origin.somefile")
    destination_file = tmpdir.join("destination.somefile")
    original_file_content = "some content"
    original_file.write(original_file_content)

    # System under test
    symlink_file(original_file, destination_file)

    # Verification
    assert os.path.islink(destination_file)
    assert os.path.realpath(destination_file) == original_file


def test_symlink_file_fail_none():
    with pytest.raises(RuntimeError):
        # System under test
        symlink_file(None, None)


def test_symlink_file_fail_with_existing_destination_file(tmpdir):
    # Setup
    original_file = tmpdir.join("origin.somefile")
    destination_file = tmpdir.join("destination.somefile")
    destination_file.write("some content")

    with pytest.raises(RuntimeError):
        # System under test
        symlink_file(original_file, destination_file)


"""
Unsymlink file tests
"""


def test_unsymlink_file_success(tmpdir):
    # Setup
    original_file = tmpdir.join("origin.somefile")
    destination_file = tmpdir.join("destination.somefile")
    original_file_content = "some content"
    original_file.write(original_file_content)
    symlink_file(original_file, destination_file)

    # Verification of setup
    assert os.path.islink(destination_file)
    assert os.path.realpath(destination_file) == original_file

    # System under test
    unsymlink_file(destination_file)

    # Verification
    assert not os.path.islink(destination_file)
    assert os.path.isfile(original_file)  # Makes sure the original file wasn't removed in the unlink


def test_unsymlink_file_fail_none():
    with pytest.raises(RuntimeError):
        # System under test
        unsymlink_file(None)


"""
Run script tests
"""


def test_run_file_success(tmpdir):
    # Setup
    some_script_file = tmpdir.join("test.sh")
    destination_file = tmpdir.join("destination_file.somefile")
    some_script_file.write(f"#!/usr/bin/env bash\necho \"Hello World!\" > {destination_file}\n")
    some_script_file.chmod(0o700)

    # System under test
    run_file(some_script_file.realpath().__str__())

    # Verification
    assert os.path.isfile(destination_file)
    destination_file_content = destination_file.read()
    assert "Hello World!\n" == destination_file_content


def test_run_file_fail_none():
    with pytest.raises(RuntimeError):
        # System under test
        run_file(None)


def test_run_file_fail_no_execution_bit_set(tmpdir):
    # Setup
    some_script_file = tmpdir.join("test.sh")
    destination_file = tmpdir.join("destination_file.somefile")
    some_script_file.write(f"#!/usr/bin/env bash\necho \"Hello World!\" > {destination_file}\n")

    with pytest.raises(RuntimeError):
        # System under test
        run_file(some_script_file)


"""
Run command tests
"""


def test_run_command_success(tmpdir):
    # Setup
    some_file = tmpdir.join("test.txt")
    some_file.write("testing")

    # Setup
    output = run_command("ls " + tmpdir.realpath().__str__())

    # Verification
    assert output == "test.txt"


def test_run_command_fail_none():
    with pytest.raises(RuntimeError):
        # System under test
        run_command(None)


def test_run_command_fail_executable_not_found_in_path():
    with pytest.raises(RuntimeError):
        # System under test
        run_command("commandabc")


"""
File moved check tests
"""


def test_file_moved_check_success(tmpdir):
    # Setup
    original_file = tmpdir.join("origin.somefile")
    destination_file = tmpdir.join("destination.somefile")
    original_file_content = "some content"
    original_file.write(original_file_content)
    mv_file(original_file, destination_file)

    # System under test
    is_file_moved = is_moved(original_file, destination_file)

    # Verification
    assert is_file_moved is True


def test_file_moved_check_fail_destination_file_does_not_exists(tmpdir):
    # Setup
    original_file = tmpdir.join("origin.somefile")
    destination_file = tmpdir.join("destination.somefile")
    original_file_content = "some content"
    original_file.write(original_file_content)

    # System under test
    is_file_moved = is_moved(original_file, destination_file)

    # Verification
    assert is_file_moved is False


def test_file_moved_check_fail_origin_file_still_exists(tmpdir):
    # Setup
    original_file = tmpdir.join("origin.somefile")
    destination_file = tmpdir.join("destination.somefile")
    original_file_content = "some content"
    original_file.write(original_file_content)

    # System under test
    is_file_moved = is_moved(original_file, destination_file)

    # Verification
    assert is_file_moved is False


"""
Broken link check tests
"""


def test_broken_link_check_success(tmpdir):
    # Setup
    original_file = tmpdir.join("origin.somefile")
    destination_file = tmpdir.join("destination.somefile")
    original_file_content = "some content"
    original_file.write(original_file_content)
    symlink_file(original_file, destination_file)
    original_file.remove()

    # System under test
    is_link_broken = is_broken_link(destination_file)

    # Verification
    assert is_link_broken is True


def test_broken_link_check_fail_normal_symlink(tmpdir):
    # Setup
    original_file = tmpdir.join("origin.somefile")
    destination_file = tmpdir.join("destination.somefile")
    original_file_content = "some content"
    original_file.write(original_file_content)
    symlink_file(original_file, destination_file)

    # System under test
    is_link_broken = is_broken_link(destination_file)

    # Verification
    assert is_link_broken is False


def test_broken_link_check_fail_normal_file(tmpdir):
    # Setup
    original_file = tmpdir.join("origin.somefile")
    original_file_content = "some content"
    original_file.write(original_file_content)

    # System under test
    is_link_broken = is_broken_link(original_file)

    # Verification
    assert is_link_broken is False


"""
Symlink check tests
"""


def test_symlink_check_success(tmpdir):
    # Setup
    original_file = tmpdir.join("origin.somefile")
    destination_file = tmpdir.join("destination.somefile")
    original_file_content = "some content"
    original_file.write(original_file_content)
    symlink_file(original_file, destination_file)

    # System under test
    is_files_linked = is_linked(original_file, destination_file)

    # Verification
    assert is_files_linked is True


def test_symlink_check_fail_normal_file(tmpdir):
    # Setup
    original_file = tmpdir.join("origin.somefile")
    destination_file = tmpdir.join("destination.somefile")
    file_content = "some content"
    destination_file.write(file_content)
    original_file.write(file_content)

    # System under test
    is_files_linked = is_linked(original_file, destination_file)

    # Verification
    assert is_files_linked is False


"""
Copy check tests
"""


def test_copy_check_success(tmpdir):
    # Setup
    original_file = tmpdir.join("origin.somefile")
    destination_file = tmpdir.join("destination.somefile")
    original_file_content = "some content"
    original_file.write(original_file_content)
    copy_file(original_file, destination_file)

    # System under test
    is_files_copied = is_copied(original_file, destination_file)

    # Verification
    assert is_files_copied is True


def test_copy_check_fail_symlink(tmpdir):
    # Setup
    original_file = tmpdir.join("origin.somefile")
    destination_file = tmpdir.join("destination.somefile")
    original_file_content = "some content"
    original_file.write(original_file_content)
    symlink_file(original_file, destination_file)

    # System under test
    is_files_copied = is_copied(original_file, destination_file)

    # Verification
    assert is_files_copied is False


def test_copy_check_fail_no_destination_file(tmpdir):
    # Setup
    original_file = tmpdir.join("origin.somefile")
    destination_file = tmpdir.join("destination.somefile")

    # System under test
    is_files_copied = is_copied(original_file, destination_file)

    # Verification
    assert is_files_copied is False


def test_copy_check_fail_different_file_sizes(tmpdir):
    # Setup
    original_file = tmpdir.join("origin.somefile")
    destination_file = tmpdir.join("destination.somefile")
    original_file_content = "some content"
    original_file.write(original_file_content)
    destination_file_content = "some other content"
    destination_file.write(destination_file_content)

    # System under test
    is_files_copied = is_copied(original_file, destination_file)

    # Verification
    assert is_files_copied is False


def test_copy_check_fail_different_metadata(tmpdir):
    # Setup
    original_file = tmpdir.join("origin.somefile")
    destination_file = tmpdir.join("destination.somefile")
    same_file_content = "same content"
    original_file.write(same_file_content)
    destination_file.write(same_file_content)

    original_file_modified_time = os.path.getmtime(original_file)
    modified_time = original_file_modified_time + 1
    os.utime(destination_file, (modified_time, modified_time))

    # System under test
    is_files_copied = is_copied(original_file, destination_file)

    # Verification
    assert is_files_copied is False


"""
Exceution check tests
"""


def test_execution_check_success(tmpdir):
    # Setup
    some_script_file = tmpdir.join("test.sh")
    some_script_file.write(f"#!/usr/bin/env bash\necho \"Hello World!\"\n")
    some_script_file.chmod(0o700)

    # System under test
    is_file_executable = is_executable(some_script_file)

    # Verification
    assert is_file_executable is True


def test_execution_check_fail_no_execution_permission(tmpdir):
    # Setup
    some_script_file = tmpdir.join("test.sh")
    some_script_file.write(f"#!/usr/bin/env bash\necho \"Hello World!\"\n")

    # System under test
    is_file_executable = is_executable(some_script_file)

    # Verification
    assert is_file_executable is False
