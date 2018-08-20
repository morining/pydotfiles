# General imports
import os
import os.path
import shutil
from subprocess import Popen, PIPE, TimeoutExpired

# Project imports
from .general import hash_file


"""
I/O-related public access helper methods
"""


def mv_file(origin, destination, use_sudo=False, sudo_password=""):
    if use_sudo:
        command = f"mv {origin} {destination}"
        process = Popen(['sudo', '-S'] + command.split(), stdin=PIPE, stderr=PIPE, universal_newlines=True)

        try:
            stdout, stderr = process.communicate(sudo_password + '\n', timeout=3)

            if "File exists" in stderr:
                raise FileExistsError(f"The file {destination} already exists")

            if process.returncode != 0:
                raise RuntimeError(stderr)
        except TimeoutExpired:
            process.kill()
            raise
    else:
        shutil.move(origin, destination)


def rm_file(file, use_sudo=False, sudo_password=""):
    # Fast return if there is no need for the operation
    if not os.path.isfile(file) and not is_broken_link(file):
        return

    if use_sudo:
        command = f"rm {file}"
        process = Popen(['sudo', '-S'] + command.split(), stdin=PIPE, stderr=PIPE, universal_newlines=True)

        try:
            stdout, stderr = process.communicate(sudo_password + '\n', timeout=3)

            if process.returncode != 0:
                raise RuntimeError(stderr)
        except TimeoutExpired:
            process.kill()
            raise
    else:
        os.unlink(file)


def copy_file(origin, destination, use_sudo=False, sudo_password=""):
    # Fast return if there is no need for the operation
    if is_copied(origin, destination):
        return

    if use_sudo:
        command = f"cp {origin} {destination}"
        process = Popen(['sudo', '-S'] + command.split(), stdin=PIPE, stderr=PIPE, universal_newlines=True)

        try:
            stdout, stderr = process.communicate(sudo_password + '\n', timeout=3)

            if "File exists" in stderr:
                raise FileExistsError(f"The file {destination} already exists")

            if process.returncode != 0:
                raise RuntimeError(stderr)
        except TimeoutExpired:
            process.kill()
            raise
    else:
        shutil.copy2(origin, destination)


def symlink_file(origin, destination, use_sudo=False, sudo_password=""):
    # Fast return if there is no need for the operation
    if is_linked(origin, destination):
        return

    if use_sudo:
        command = f"ln -s {origin} {destination}"
        process = Popen(['sudo', '-S'] + command.split(), stdin=PIPE, stderr=PIPE, universal_newlines=True)

        try:
            stdout, stderr = process.communicate(sudo_password + '\n', timeout=3)

            if "File exists" in stderr:
                raise FileExistsError(f"The file {destination} already exists")

            if process.returncode != 0:
                raise RuntimeError(stderr)
        except TimeoutExpired:
            process.kill()
            raise
    else:
        os.symlink(origin, destination)


def unsymlink_file(origin, destination, use_sudo=False, sudo_password=""):
    # Fast return if there is no need for the operation
    if not is_linked(origin, destination):
        return

    if use_sudo:
        command = f"unlink {destination}"
        process = Popen(['sudo', '-S'] + command.split(), stdin=PIPE, stderr=PIPE, universal_newlines=True)

        try:
            stdout, stderr = process.communicate(sudo_password + '\n', timeout=3)

            if "File exists" in stderr:
                raise FileExistsError(f"The file {destination} already exists")

            if process.returncode != 0:
                raise RuntimeError(stderr)
        except TimeoutExpired:
            process.kill()
            raise
    else:
        os.unlink(destination)


"""
Utility functions
"""


def is_broken_link(file):
    return os.path.islink(file) and not os.path.exists(file)


def is_linked(origin, destination):
    return os.path.islink(destination) and os.path.realpath(destination) == os.path.realpath(origin)


def is_copied(origin, destination):
    # Enables fast-failing based on existence
    if not os.path.isfile(destination):
        return False

    # Enables fast-failing based on file size
    origin_file_size = os.stat(origin).st_size
    destination_file_size = os.stat(destination).st_size

    if origin_file_size != destination_file_size:
        return False

    # Enables fast-failing based on metadata
    origin_last_modified_time = os.path.getmtime(origin)
    destination_last_modified_time = os.path.getmtime(destination)

    if origin_last_modified_time != destination_last_modified_time:
        return False

    # Loads in the files and checks that their hashes are the same
    origin_file_hash = hash_file(origin)
    destination_file_hash = hash_file(destination)
    return origin_file_hash == destination_file_hash
