# General imports
from argparse import Namespace

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
    def download(request: Namespace) -> Response:
        set_logging(request.quiet, request.verbose)
        return DownloadHandler.download(request)

    @staticmethod
    def install(request: Namespace) -> Response:
        set_logging(request.quiet, request.verbose)
        return InstallationHandler.install(request)

    @staticmethod
    def uninstall(request: Namespace) -> Response:
        set_logging(request.quiet, request.verbose)
        return InstallationHandler.uninstall(request)

    @staticmethod
    def update(request: Namespace) -> Response:
        set_logging(request.quiet, request.verbose)
        return UpdateHandler.update(request)

    @staticmethod
    def clean(request: Namespace) -> Response:
        set_logging(request.quiet, request.verbose)
        return CleanHandler.clean(request)

    @staticmethod
    def configure(request: Namespace) -> Response:
        set_logging(request.quiet, request.verbose)
        return ConfigureHandler.configure(request)

    @staticmethod
    def validate(request: Namespace) -> Response:
        set_logging(request.quiet, request.verbose)
        return ValidateHandler.validate(request)
