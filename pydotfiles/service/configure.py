# General imports
from argparse import Namespace
from pathlib import Path

# Project imports
from .common import Response
from .common import ResponseCode
from .common import SettingsManager


class ConfigureHandler:

    @staticmethod
    def configure(request: Namespace) -> Response:
        local_directory = request.local_directory
        remote_repo = request.remote_repo

        if local_directory is None and remote_repo is None:
            local_directory = SettingsManager.get_local_directory()
            remote_repo = SettingsManager.get_remote_repo()
            response_message = f"Configure: No configuration setting passed in [local_directory={local_directory}, remote_repo={remote_repo}]"
            return Response(ResponseCode.OK_RESPONSE, response_message)

        if local_directory is not None:
            SettingsManager.set_local_directory(Path(local_directory))

        if remote_repo is not None:
            SettingsManager.set_remote_repo(remote_repo)

        local_directory = SettingsManager.get_local_directory()
        remote_repo = SettingsManager.get_remote_repo()

        response_message = f"Configure: Successfully persisted configuration data [local_directory={local_directory}, remote_repo={remote_repo}]"
        return Response(ResponseCode.OK_RESPONSE, response_message)
