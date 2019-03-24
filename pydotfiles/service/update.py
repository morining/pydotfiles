# General imports
from argparse import Namespace
from enum import Enum

# Project imports
from .common import ContextualError
from .common import Response


class UpdateHandler:

    @staticmethod
    def update(request: Namespace) -> Response:
        #
        # config_repo_local, config_repo_remote = load_pydotfiles_config_data(CacheDirectory())
        #
        # self.dotfiles = Dotfiles(config_repo_local, config_repo_remote, args.quiet, args.verbose)
        #
        # if not self.dotfiles.is_cloned:
        #     PrettyPrint.fail(f"Update: Could not update- no dotfiles detected")
        #
        # self.dotfiles.update()
        pass


class UpdatingErrorEnum(Enum):
    ERROR_REASON_A = "help message in response to error reason A"
    ERROR_REASON_B = "help message in response to error reason B"
    ERROR_REASON_C = "help message in response to error reason C"
