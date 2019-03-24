# General imports
from pathlib import Path
from typing import Dict

# Project imports
from .common import Response
from .common import ResponseCode
from .common import SettingsManager


class ConfigureHandler:

    @staticmethod
    def configure(request: Dict) -> Response:
        local_directory = request.get("local_directory")
        remote_repo = request.get("remote_repo")

        if local_directory is None and remote_repo is None:
            current_local_directory = SettingsManager.get_local_directory()
            current_remote_repo = SettingsManager.get_remote_repo()
            response_message = f"Configure: No configuration setting passed in [current_local_directory={current_local_directory}, current_remote_repo={current_remote_repo}]"
            return Response(ResponseCode.OK_RESPONSE, response_message)

        if local_directory is not None:
            SettingsManager.set_local_directory(Path(local_directory))

        if remote_repo is not None:
            SettingsManager.set_remote_repo(remote_repo)

        local_directory = SettingsManager.get_local_directory()
        remote_repo = SettingsManager.get_remote_repo()

        response_message = f"Configure: Successfully persisted configuration data [local_directory={local_directory}, remote_repo={remote_repo}]"
        return Response(ResponseCode.OK_RESPONSE, response_message)
