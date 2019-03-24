# General imports
from typing import Dict
from logging import getLogger

# Vendor imports
from git import Repo
from git.exc import GitCommandError

# Project imports
from .common import ContextualError
from .common import Response
from .common import ResponseCode
from .common import SettingsManager
from .common import DEFAULT_PYDOTFILES_REMOTE_REPO
from .configure import ConfigureHandler
from pydotfiles.git import GitRemoteProgress
from pydotfiles.git import GitErrorToHelpMessageMapper


logger = getLogger(__name__)


class DownloadHandler:

    @staticmethod
    def download(request: Dict) -> Response:
        ConfigureHandler.configure(request)

        local_directory = SettingsManager.get_local_directory()
        remote_repo = SettingsManager.get_remote_repo()

        if DownloadHandler.is_cloned():
            response_message = f"Download: Dotfiles have already been cloned"
            return Response(ResponseCode.OK_RESPONSE, response_message)

        if remote_repo == DEFAULT_PYDOTFILES_REMOTE_REPO:
            logger.warning(f"Download: Using the default base configuration settings from {DEFAULT_PYDOTFILES_REMOTE_REPO}- If you'd like to instead download your own dotfiles (and persist the remote link for future use), try running:\n\npydotfiles clean repo # (removes the just-downloaded dotfile config)\npydotfiles download --remote-repo <git remote link>\n\nEXAMPLE:\npydotfiles download --remote-repo git@github.com:JasonYao/dotfiles.git\n\n")

        logger.info(f"Download: Cloning git repository")
        logger.debug(f"remote_repo={remote_repo}, local_directory={local_directory}")
        try:
            Repo.clone_from(remote_repo, local_directory, progress=GitRemoteProgress())
            response_message = f"Download: Successfully cloned git repository"
            return Response(ResponseCode.OK_RESPONSE, response_message)
        except GitCommandError as e:
            response_message = f"Download: Failed to clone git repository"
            logger.debug(e)
            reason = GitErrorToHelpMessageMapper.get_help_message(e.status)
            contextual_error = ContextualError(ResponseCode.REMOTE_REPO_CLONE_ISSUE, response_message, {
                "remote_repo": remote_repo,
                "local_directory": local_directory,
                "error_reason": reason,
            })
            return Response.from_contextual_error(contextual_error)
        except Exception as e:
            response_message = f"Download: Failed to clone git repository"
            logger.debug(e)
            contextual_error = ContextualError(ResponseCode.REMOTE_REPO_CLONE_ISSUE, response_message, {
                "remote_repo": remote_repo,
                "local_directory": local_directory,
            })
            return Response.from_contextual_error(contextual_error)

    @staticmethod
    def is_cloned() -> bool:
        local_directory = SettingsManager.get_local_directory()
        return local_directory.joinpath(".git").is_dir()
