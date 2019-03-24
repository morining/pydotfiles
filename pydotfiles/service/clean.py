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
            clean_response = CleanHandler.clean_target(clean_target_path)
            return Response(ResponseCode.OK_RESPONSE, clean_response)
        except ContextualError as e:
            return Response.from_contextual_error(e)
        except OSError as e:
            logger.error(f"Clean: An unknown IO error occurred")
            contextual_error = ContextualError(ResponseCode.UNKNOWN_CLEANING_ERROR, str(e), {
                "directory_cleanup_target": clean_target_path
            })
            return Response.from_contextual_error(contextual_error)

    @staticmethod
    def get_target_path(target: str) -> Path:
        if target == "cache":
            return SettingsManager.get_cache_path()
        elif target == "repo":
            return SettingsManager.get_local_directory()
        else:
            raise ContextualError(ResponseCode.UNKNOWN_CLEANING_TARGET, f"Clean: Unknown cleaning target passed in [target={target}]")

    @staticmethod
    def clean_target(target: Path) -> str:
        if target.is_dir():
            logger.debug(f"Clean: Cleaning the directory [target={target}]")
            rmtree(target)
            return f"Clean: Successfully cleaned out the directory [target={target}]"
        else:
            return f"Clean: The directory has already been cleaned [target={target}]"
