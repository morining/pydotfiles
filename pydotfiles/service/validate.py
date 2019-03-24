# General imports
from argparse import Namespace
from enum import Enum

# Project imports
from .common import ContextualError
from .common import Response


class ValidateHandler:

    @staticmethod
    def validate(request: Namespace) -> Response:
        #
        # validator = Validator(args.quiet, args.verbose)
        # try:
        #     validator.validate_directory(args.directory)
        # except ValidationError as e:
        #     PrettyPrint.fail(e.help_message)
        pass


class ValidateErrorEnum(Enum):
    ERROR_REASON_A = "help message in response to error reason A"
    ERROR_REASON_B = "help message in response to error reason B"
    ERROR_REASON_C = "help message in response to error reason C"
