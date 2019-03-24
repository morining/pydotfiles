# General imports
from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter
from typing import Callable
from pathlib import Path
from typing import Dict

# Project imports
from pydotfiles.version import VERSION_NUMBER
from pydotfiles.service import ServiceDelegator
from pydotfiles.service import Response
from pydotfiles.service.common import DEFAULT_PYDOTFILES_CACHE_DIRECTORY
from pydotfiles.service.common import DEFAULT_PYDOTFILES_LOCAL_DIRECTORY
from pydotfiles.service.common import DEFAULT_PYDOTFILES_REMOTE_REPO
from pydotfiles.utils.general import PrettyPrint


class ArgumentDispatcher:
    """
    A presentation-layer class to contain all logic around
    using the pydotfiles API, providing help menus and
    simplifying argument-parsing via dynamic dispatching
    of commands
    """

    @staticmethod
    def dispatch(api_arguments) -> None:
        valid_commands = [
            'download',
            'install',
            'uninstall',
            'update',
            'clean',
            'configure',
            'validate',
        ]

        parser = ArgumentParser(formatter_class=RawDescriptionHelpFormatter, description="""
        Python Dotfiles Manager, enabling configuration-based management of your system!

        Commands:
          - download: Downloads your dotfiles onto your computer
          - install: Installs all/part of your dotfiles
          - uninstall: Uninstalls all/part of your dotfiles
          - update: Updates all/part of your dotfiles
          - clean: Removes the pydotfiles cache/default
          - configure: Sets configuration values for managing your dotfiles
          - validate: Validates that a given directory is pydotfiles-compliant
        """)
        parser.add_argument('--version', action='version', version='%(prog)s ' + VERSION_NUMBER)
        parser.add_argument("command", help="Runs the command given", choices=valid_commands)

        command = api_arguments[1:2]
        command_arguments = api_arguments[2:]

        args = parser.parse_args(command)

        # Dynamically dispatches to the relevant method
        getattr(ArgumentDispatcher, args.command)(command_arguments)

    @staticmethod
    def download(command_arguments) -> None:
        help_description = f"""
        Downloads the dotfiles config repo if it hasn't been cloned to local.

        If a remote repo is not provided pydotfiles will use the basic set of pydotfiles
        found at https://github.com/JasonYao/pydotfiles-basic.

        Pydotfiles's configuration is setup in a fallthrough manner:
            - Command-line arguments passed in override all other configs, and will be persisted in $HOME/.pydotfiles/config.json
            - Any non-overridden arguments is then configured from: $HOME/.pydotfiles/config.json (if it exists)
            - Any remaining arguments will default to:
                - Local directory: {DEFAULT_PYDOTFILES_LOCAL_DIRECTORY}
                - Remote repo: {DEFAULT_PYDOTFILES_REMOTE_REPO}
        """
        parser = get_base_parser(help_description, "download")
        parser.add_argument("-l", "--local-directory", help="The local directory where the dotfiles are stored")
        parser.add_argument("-r", "--remote-repo", help="The local directory where the dotfiles are stored")
        args = parser.parse_args(command_arguments)

        send_to_service_delegator(vars(args), ServiceDelegator.download)

    @staticmethod
    def install(command_arguments) -> None:
        help_description = """
        Installs your dotfile's modules (default: installs all modules)
        NOTE: Your dotfiles need to have first been downloaded via `pydotfiles download` beforehand
        """
        parser = get_base_parser(help_description, "install")
        parser.add_argument("-m", "--modules", help="A list of specific modules to install", nargs="+")
        args = parser.parse_args(command_arguments)

        send_to_service_delegator(vars(args), ServiceDelegator.install)

    @staticmethod
    def uninstall(command_arguments) -> None:
        help_description = """
        Uninstalls your dotfile's modules (default: uninstalls all modules, but leaves packages, applications, and dev-environments alone)
        """
        parser = get_base_parser(help_description, "uninstall")
        parser.add_argument("-m", "--modules", help="A list of specific modules to uninstall", nargs="+")
        parser.add_argument("-p", "--uninstall-packages", help="Will uninstall all packages installed with these module(s)", action="store_true")
        parser.add_argument("-a", "--uninstall-applications", help="Will uninstall all applications installed with these module(s)", action="store_true")
        parser.add_argument("-e", "--uninstall-environments", help="Will uninstall all dev environments with these module(s)", action="store_true")
        args = parser.parse_args(command_arguments)

        send_to_service_delegator(vars(args), ServiceDelegator.uninstall)

    @staticmethod
    def update(command_arguments) -> None:
        help_description = """
        Updates the local dotfiles from the remote repo
        """
        parser = get_base_parser(help_description, "update")
        args = parser.parse_args(command_arguments)

        send_to_service_delegator(vars(args), ServiceDelegator.update)

    @staticmethod
    def clean(command_arguments) -> None:
        help_description = f"""
        Deletes either the pydotfiles cache or the downloaded local dotfiles config repo

        Possible choices:
            - cache: Deletes everything in the pydotfiles cache directory ({DEFAULT_PYDOTFILES_CACHE_DIRECTORY})
            - repo: Deletes everything in the locally downloaded dotfiles configuration directory ({DEFAULT_PYDOTFILES_LOCAL_DIRECTORY})
        """
        valid_cleaning_targets = ['cache', 'repo']
        parser = get_base_parser(help_description, "clean")
        parser.add_argument('clean_target', help='Clears out the given cleaning target', choices=valid_cleaning_targets)
        args = parser.parse_args(command_arguments)

        send_to_service_delegator(vars(args), ServiceDelegator.clean)

    @staticmethod
    def configure(command_arguments) -> None:
        help_description = f"""
        Enables direct configuration of pydotfile's default values
        """
        parser = get_base_parser(help_description, "set")
        parser.add_argument("-l", "--local-directory", help="Sets the dotfiles configuration repo to a different local directory")
        parser.add_argument("-r", "--remote-repo", help="Sets pydotfiles to point to a different remote repo")
        args = parser.parse_args(command_arguments)

        send_to_service_delegator(vars(args), ServiceDelegator.configure)

    @staticmethod
    def validate(command_arguments) -> None:
        help_description = """
        Validates a given directory and whether it's pydotfiles-compliant.
        (default: Checks the current working directory)
        """
        parser = get_base_parser(help_description, "validate")
        parser.add_argument("-d", "--directory", help="Validates the passed in directory", default=Path.cwd())

        args = parser.parse_args(command_arguments)

        send_to_service_delegator(vars(args), ServiceDelegator.validate)


"""
Helper methods
"""


def get_base_parser(description: str, sub_command: str) -> ArgumentParser:
    parser = ArgumentParser(
        prog=f"pydotfiles {sub_command}",
        formatter_class=RawDescriptionHelpFormatter,
        description=description
    )
    logging_parser_group = parser.add_mutually_exclusive_group()
    logging_parser_group.add_argument("-v", "--verbose", help="Enables more verbose logging", action="store_true")
    logging_parser_group.add_argument("-q", "--quiet", help="Squelches the default logging (still outputs to stderr upon failures)", action="store_true")
    return parser


def send_to_service_delegator(request: Dict, delegated_function: Callable[[Dict], Response]) -> None:
    response = delegated_function(request)

    if response.is_ok:
        PrettyPrint.success(response.response_message)
    else:
        PrettyPrint.fail(response.error.help_message)
