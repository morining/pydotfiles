# General imports
from argparse import Namespace
from enum import Enum

# Project imports
from .common import ContextualError
from .common import Response


class DownloadHandler:

    @staticmethod
    def download(request: Namespace) -> Response:
        # # TODO P4: Add in cleaner signature
        # config_repo_local, config_repo_remote = get_pydotfiles_config_data_with_override(args.local_directory,
        #                                                                                  args.remote_repo,
        #                                                                                  CacheDirectory())
        #
        # self.dotfiles = Dotfiles(config_repo_local, config_repo_remote, args.quiet, args.verbose)
        #
        # if self.dotfiles.is_cloned:
        #     PrettyPrint.success(f"Clone: Dotfiles have already been cloned")
        #     return
        #
        # try:
        #     self.dotfiles.download()
        # except PydotfilesError as e:
        #     PrettyPrint.fail(e.help_message)
        pass


class DownloadErrorEnum(Enum):
    ERROR_REASON_A = "help message in response to error reason A"
    ERROR_REASON_B = "help message in response to error reason B"
    ERROR_REASON_C = "help message in response to error reason C"
