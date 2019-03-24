# General imports
from typing import Dict

# Project imports
from .common import ContextualError
from .common import Response
from .clean import CleanHandler
from .download import DownloadHandler
from .installation import InstallationHandler
from .configure import ConfigureHandler
from .update import UpdateHandler
from .validate import ValidateHandler

# TODO cleanup
from pydotfiles.models.utils import set_logging


class ServiceDelegator:

    @staticmethod
    def download(request: Dict) -> Response:
        set_logging(request.get("quiet"), request.get("verbose"))
        return DownloadHandler.download(request)

    @staticmethod
    def install(request: Dict) -> Response:
        set_logging(request.get("quiet"), request.get("verbose"))
        return InstallationHandler.install(request)

    @staticmethod
    def uninstall(request: Dict) -> Response:
        set_logging(request.get("quiet"), request.get("verbose"))
        return InstallationHandler.uninstall(request)

    @staticmethod
    def update(request: Dict) -> Response:
        set_logging(request.get("quiet"), request.get("verbose"))
        return UpdateHandler.update(request)

    @staticmethod
    def clean(request: Dict) -> Response:
        set_logging(request.get("quiet"), request.get("verbose"))
        return CleanHandler.clean(request)

    @staticmethod
    def configure(request: Dict) -> Response:
        set_logging(request.get("quiet"), request.get("verbose"))
        return ConfigureHandler.configure(request)

    @staticmethod
    def validate(request: Dict) -> Response:
        set_logging(request.get("quiet"), request.get("verbose"))
        return ValidateHandler.validate(request)
