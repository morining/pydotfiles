# General imports
from argparse import Namespace
from logging import getLogger
from shutil import rmtree
from pathlib import Path

# Project imports
from .common import ContextualError
from .common import Response
from .common import ResponseCode
from .common import SettingsManager


logger = getLogger(__name__)


class CleanHandler:

    @staticmethod
    def clean(request: Namespace) -> Response:
        clean_target = request.clean_target

        try:
            clean_target_path = CleanHandler.get_target_path(clean_target)
            CleanHandler.clean_target(clean_target_path)
            response_message = f"Clean: Successfully cleaned out directory [directory={clean_target_path}]"
            return Response(ResponseCode.OK_RESPONSE, response_message)
        except ContextualError as e:
            return Response(e.reason, e.message, e)

    @staticmethod
    def get_target_path(target: str) -> Path:
        if target == "cache":
            return SettingsManager.get_cache_path()
        elif target == "repo":
            return SettingsManager.get_local_directory()
        else:
            raise ContextualError(ResponseCode.UNKNOWN_CLEANING_TARGET, f"Clean: Unknown cleaning target passed in [target={target}]")

    @staticmethod
    def clean_target(target: Path) -> None:
        if target.is_dir():
            logger.info(f"Clean: Deleting the directory [target={target}]")
            rmtree(target)
            logger.info(f"Clean: Successfully deleted the directory [target={target}]")
        else:
            logger.info(f"Clean: The directory has already been cleaned [target={target}]")
