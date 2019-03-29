# General imports
from argparse import Namespace
from enum import Enum
from typing import Dict
from logging import getLogger

# Vendor imports
from git import Repo
from git import GitCommandError

# Project imports
from .common import ContextualError
from .common import Response
from .common import SettingsManager
from .common import ResponseCode
from .download import DownloadHandler
from pydotfiles.git import GitRemoteProgress
from pydotfiles.git import GitErrorToHelpMessageMapper


logger = getLogger(__name__)


class UpdateHandler:

    @staticmethod
    def update(request: Dict) -> Response:
        local_directory = SettingsManager.get_local_directory()
        remote_repo = SettingsManager.get_remote_repo()

        if not DownloadHandler.is_cloned():
            response_message = f"Update: Failed to update local dotfiles to latest origin master (no local dotfiles detected)"
            return Response(ResponseCode.NO_LOCAL_REPO_FOUND, response_message)

        try:
            Repo(local_directory).remote('origin').pull(progress=GitRemoteProgress())
            response_message = f"Update: Successfully updated local dotfiles repo with the latest remote changes"
            return Response(ResponseCode.OK_RESPONSE, response_message)
        except GitCommandError as e:
            response_message = f"Update: Failed to update local dotfiles repo with the latest remote changes"
            logger.debug(e)
            reason = GitErrorToHelpMessageMapper.get_help_message(e.status)
            contextual_error = ContextualError(ResponseCode.REMOTE_REPO_CLONE_ISSUE, response_message, {
                "remote_repo": remote_repo,
                "local_directory": local_directory,
                "error_reason": reason,
            })
            return Response.from_contextual_error(contextual_error)
        except Exception as e:
            response_message = f"Update: Failed to update local dotfiles repo with the latest remote changes"
            logger.debug(e)
            contextual_error = ContextualError(ResponseCode.REMOTE_REPO_CLONE_ISSUE, response_message, {
                "remote_repo": remote_repo,
                "local_directory": local_directory,
            })
            return Response.from_contextual_error(contextual_error)
