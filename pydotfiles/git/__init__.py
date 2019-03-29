# General imports
from typing import Optional

# Vendor imports
from git.remote import RemoteProgress
from progressbar import ProgressBar
from git import GitCommandError

# Project imports
from pydotfiles.service.common import ResponseCode


class GitRemoteProgress(RemoteProgress):
    """
    An object passed as a callback that will display
    a progressbar while downloading files from the git
    remote
    """

    def __init__(self):
        super().__init__()
        self.progress_bar = None
        self.is_done = False

    def update(self, op_code, cur_count, max_count=None, message=''):
        if self.is_done:
            return

        if self.progress_bar is None:
            self.progress_bar = ProgressBar(max_value=max_count)
            self.progress_bar.start()

        if cur_count == max_count:
            self.progress_bar.finish()
            self.is_done = True
        else:
            self.progress_bar.update(cur_count)


class GitErrorToHelpMessageMapper:
    """
    A static mapper to help retrieve a user-friendly
    help message given a git error that occurred
    """

    git_error_to_reason_map = {
        "Your local changes to the following files would be overwritten by merge": ResponseCode.LOCAL_CHANGES_TO_GIT_REPO_PREVENTING_UPDATE,
        "Could not read from remote repository": ResponseCode.COULD_NOT_ACCESS_REMOTE_REPO,
    }

    @staticmethod
    def get_error_message(error: GitCommandError) -> str:
        return error.stderr.strip().replace("'", "").replace("stderr:", "").replace("Aborting", "").strip()

    @staticmethod
    def get_error_reason(error: GitCommandError) -> Optional[ResponseCode]:
        # NOTE: We have to parse from the error message since GitPython is shit and
        # has a status code that is just 1, instead of something useful
        error_message = GitErrorToHelpMessageMapper.get_error_message(error)

        for git_error, response_code in GitErrorToHelpMessageMapper.git_error_to_reason_map.items():
            if git_error in error_message:
                return response_code
        return None
