# General imports
from argparse import Namespace
from enum import Enum

# Project imports
from .common import ContextualError
from .common import Response


class InstallationHandler:

    @staticmethod
    def install(request: Namespace) -> Response:
        #
        # # TODO P4: Add in cleaner signature
        # config_repo_local, config_repo_remote = load_pydotfiles_config_data(CacheDirectory())
        #
        # self.dotfiles = Dotfiles(config_repo_local, config_repo_remote, args.quiet, args.verbose, args.modules)
        #
        # if not self.dotfiles.is_cloned:
        #     PrettyPrint.fail(f"Install: No dotfiles detected, please download it first with `pydotfiles download`")
        #
        # if args.modules is None:
        #     self.dotfiles.install_all()
        # else:
        #     self.dotfiles.install_multiple_modules(args.modules)
        pass

    @staticmethod
    def uninstall(request: Namespace) -> Response:
        #
        # config_repo_local, config_repo_remote = load_pydotfiles_config_data(CacheDirectory())
        #
        # PrettyPrint.info(f"Uninstall: Uninstalling dotfiles")
        #
        # self.dotfiles = Dotfiles(config_repo_local, config_repo_remote, args.quiet, args.verbose, args.modules)
        #
        # if not self.dotfiles.is_cloned:
        #     PrettyPrint.fail(f"Uninstall: Could not uninstall- no dotfiles detected")
        #
        # if args.modules is None:
        #     self.dotfiles.uninstall_all(args.uninstall_packages, args.uninstall_applications, args.uninstall_environments)
        # else:
        #     self.dotfiles.uninstall_multiple_modules(args.modules, args.uninstall_packages, args.uninstall_applications, args.uninstall_environments)
        pass


class InstallationErrorEnum(Enum):
    ERROR_REASON_A = "help message in response to error reason A"
    ERROR_REASON_B = "help message in response to error reason B"
    ERROR_REASON_C = "help message in response to error reason C"


class UninstallationErrorEnum(Enum):
    ERROR_REASON_A = "help message in response to error reason A"
    ERROR_REASON_B = "help message in response to error reason B"
    ERROR_REASON_C = "help message in response to error reason C"
