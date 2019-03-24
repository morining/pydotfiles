# Vendor imports
from git.remote import RemoteProgress
from progressbar import ProgressBar


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
    message_map = {
        128: "Could not read from remote repository.\n\n Please make sure you have the correct access rights\nand the repository exists"
    }

    @staticmethod
    def get_help_message(status_code: int) -> str:
        return GitErrorToHelpMessageMapper.message_map.get(status_code)
