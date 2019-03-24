from enum import Enum
from typing import Optional
from typing import Dict
from pathlib import Path
from os import environ
from json import dumps as json_dumps
from json import load as json_load


DEFAULT_PYDOTFILES_CACHE_DIRECTORY = Path.joinpath(Path.home(), ".pydotfiles")

DEFAULT_PYDOTFILES_LOCAL_DIRECTORY = Path.joinpath(Path.home(), ".dotfiles")

DEFAULT_PYDOTFILES_REMOTE_REPO = "https://github.com/JasonYao/pydotfiles-basic.git"


class SettingsManager:

    @staticmethod
    def get_cache_path() -> Path:
        cache_directory_env_var = environ.get("PYDOTFILES_CACHE_DIRECTORY")

        if cache_directory_env_var is None:
            return DEFAULT_PYDOTFILES_CACHE_DIRECTORY
        else:
            return Path(cache_directory_env_var)

    @staticmethod
    def get_local_directory() -> Path:
        setting_cache_directory_path = SettingsManager.get_cache_path()
        cache_manager = ConfigurationCacheManager(setting_cache_directory_path)

        # Checks the cache for a usable value
        if cache_manager.config_file.is_file():
            cached_data = cache_manager.read_from_file(cache_manager.config_file)
            cached_local_directory = cached_data.get("local_directory")
            if cached_local_directory is not None:
                return Path(cached_local_directory)

        # Checks the environment variable for a usable value
        local_directory_environment_variable = environ.get("PYDOTFILES_LOCAL_DIRECTORY")
        if local_directory_environment_variable is not None:
            return Path(local_directory_environment_variable)

        # Uses the default value if nothing else is available
        return DEFAULT_PYDOTFILES_LOCAL_DIRECTORY

    @staticmethod
    def get_remote_repo() -> str:
        setting_cache_directory_path = SettingsManager.get_cache_path()
        cache_manager = ConfigurationCacheManager(setting_cache_directory_path)

        # Checks the cache for a usable value
        if cache_manager.config_file.is_file():
            cached_data = cache_manager.read_from_file(cache_manager.config_file)
            cached_remote_repo = cached_data.get("remote_repo")
            if cached_remote_repo is not None:
                return cached_remote_repo

        # Checks the environment variable for a usable value
        remote_repo_environment_variable = environ.get("PYDOTFILES_REMOTE_REPO")
        if remote_repo_environment_variable is not None:
            return remote_repo_environment_variable

        # Uses the default value if nothing else is available
        return DEFAULT_PYDOTFILES_REMOTE_REPO

    @staticmethod
    def set_local_directory(local_directory: Path) -> None:
        setting_cache_directory_path = SettingsManager.get_cache_path()
        cache_manager = ConfigurationCacheManager(setting_cache_directory_path)

        current_cache_data = cache_manager.read_from_file(cache_manager.config_file)
        current_cache_data['local_directory'] = str(local_directory)
        cache_manager.write_to_file(cache_manager.config_file, current_cache_data)

    @staticmethod
    def set_remote_repo(remote_repo: str) -> None:
        setting_cache_directory_path = SettingsManager.get_cache_path()
        cache_manager = ConfigurationCacheManager(setting_cache_directory_path)

        current_cache_data = cache_manager.read_from_file(cache_manager.config_file)
        current_cache_data['remote_repo'] = remote_repo
        cache_manager.write_to_file(cache_manager.config_file, current_cache_data)


class PackageCacheManager:
    pass


class ResponseCode(Enum):

    # General response codes
    OK_RESPONSE = 0

    # Download response codes

    # Install response codes

    # Uninstall response codes

    # Update response codes

    # Clean response codes
    UNKNOWN_CLEANING_TARGET = 5000
    UNKNOWN_CLEANING_ERROR = 5001

    # Configure response codes

    # Validate response codes

    # Loading response codes
    UNSUPPORTED_FILE_TYPE = 8000


class ContextualError(Exception):

    def __init__(self, reason: ResponseCode, message: str, context_map: Optional[Dict] = None):
        super().__init__()
        self.reason = reason
        self.message = message

        if context_map is None:
            context_map = {}
        context_map["help"] = "If you need additional context like a stack trace, please run in verbose mode (with the -v flag)"

        self.context_map = context_map

    @property
    def help_message(self) -> str:
        if len(self.context_map) == 0:
            serialized_context_decoration = ""
        else:
            serialized_context_decoration = '\n'.join([f"\t{context_type}: {context_reason}" for context_type, context_reason in self.context_map.items()])

        decorated_error_message = f"{self.message} [\n{serialized_context_decoration}\n]"
        return decorated_error_message


class Response:

    def __init__(self, response_code: ResponseCode, response_message: str, error: ContextualError = None):
        self.response_code = response_code
        self.response_message = response_message
        self.error = error

    @classmethod
    def from_contextual_error(cls, error: ContextualError):
        return cls(error.reason, error.message, error)

    @property
    def is_ok(self) -> bool:
        return self.response_code == ResponseCode.OK_RESPONSE


class ConfigurationCacheManager:
    """
    Class managing all reads/writes to the
    configuration cache
    """

    def __init__(self, cache_directory: Path):
        self.cache_directory = cache_directory

    @property
    def config_file(self) -> Path:
        return Path.joinpath(self.cache_directory, "config.json")

    @property
    def is_created(self) -> bool:
        return self.cache_directory.is_dir()

    def write_to_file(self, file: Path, data: Dict) -> None:
        self.cache_directory.mkdir(parents=True, exist_ok=True)

        with file.open('w') as config_file_fd:
            config_file_fd.write(json_dumps(data, sort_keys=True, indent=4))

    @staticmethod
    def read_from_file(file_path: Path) -> Dict:
        if not file_path.is_file():
            return {}

        with file_path.open('r') as config_file_fd:
            return json_load(config_file_fd)

#              OLD STUFF BELOW
# Turn this into a PackageCacheManager later
# class ConfigurationCacheManager:
#     """
#     Class managing all reads/writes to the
#     configuration cache
#     """
#
#     def __init__(self, package_manager=None, cache_directory=DEFAULT_PYDOTFILES_CACHE_DIRECTORY):
#         self.cache_directory = cache_directory
#         self.package_manager = package_manager
#
#         self.installed_packages = None
#         self.installed_applications = None
#
#         if package_manager is not None:
#             self.reload_packages()
#             self.reload_applications()
#
#     @property
#     def config_file(self):
#         return f"{self.cache_directory}/config.json"
#
#     @property
#     def application_cache_file(self):
#         return f"{self.cache_directory}/{self.package_manager.name.lower()}-application-cache"
#
#     @property
#     def package_cache_file(self):
#         return f"{self.cache_directory}/{self.package_manager.name.lower()}-package-cache"
#
#     @property
#     def is_created(self):
#         return os.path.isdir(self.cache_directory)
#
#     """
#     Config-file methods
#     """
#
#     def write_to_config(self, data):
#         self.__idempotent_create__()
#
#         with open(self.config_file, 'w') as config_file:
#             config_file.write(json.dumps(data, sort_keys=True, indent=4))
#
#     def read_from_config(self):
#         if not os.path.isfile(self.config_file):
#             return {}
#
#         with open(self.config_file, 'r') as config_file:
#             return json.load(config_file)
#
#     """
#     Public cache accessors
#     """
#
#     def is_package_installed(self, package):
#         if self.installed_packages is None:
#             return False
#
#         return package in self.installed_packages
#
#     def is_application_installed(self, application):
#         if self.installed_applications is None:
#             return False
#
#         return application in self.installed_applications
#
#     """
#     Public cache updaters
#     """
#
#     def overwrite_packages(self, packages):
#         self.__overwrite_cache_file__(self.package_cache_file, packages)
#
#     def overwrite_applications(self, applications):
#         self.__overwrite_cache_file__(self.application_cache_file, applications)
#
#     def append_package(self, package):
#         self.__append_to_cache_file__(self.package_cache_file, package)
#
#     def append_application(self, application):
#         self.__append_to_cache_file__(self.application_cache_file, application)
#
#     def reload_packages(self):
#         self.installed_packages = self.__read_from_cache_file__(self.package_cache_file)
#
#     def reload_applications(self):
#         self.installed_applications = self.__read_from_cache_file__(self.application_cache_file)
#
#     """
#     Internal helper methods
#     """
#
#     def __idempotent_create__(self):
#         if self.is_created:
#             logger.debug(f"Caching: Cache directory was already created [directory={self.cache_directory}]")
#             return
#
#         logger.debug(f"Caching: No cache directory was found, creating now [directory={self.cache_directory}]")
#         Path(self.cache_directory).mkdir(parents=True, exist_ok=True)
#         logger.debug(f"Caching: Successfully created cache directory [directory={self.cache_directory}]")
#
#     def __overwrite_cache_file__(self, cache_file, data):
#         self.__idempotent_create__()
#         with open(cache_file, "w") as cache_file:
#             cache_file.write(f"{data}\n")
#
#     @staticmethod
#     def __append_to_cache_file__(cache_file, data):
#         with open(cache_file, "a") as cache_file:
#             cache_file.write(f"{data}\n")
#
#     def __read_from_cache_file__(self, cache_file):
#         if os.path.isdir(self.cache_directory):
#             if os.path.isfile(cache_file):
#                 with open(cache_file) as cache_file_descriptor:
#                     cached_data = {line.rstrip('\n') for line in cache_file_descriptor}
#                     logger.debug(f"Caching: Loaded in cache data [file={cache_file}, data={cached_data}")
#                     return cached_data
#             else:
#                 logger.debug(f"Caching: No cache file found [file={cache_file}]")
#         else:
#             logger.debug(f"Caching: No cache directory found [directory={self.cache_directory}]")
#         return None


"""
Old methods copied over
"""


# def clean(target):
#     """
#     Deletes the downloaded dotfile configs directory
#     """


# def load_pydotfiles_config_data(cach_directory: CacheDirectory):
#     config_local_directory = DEFAULT_PYDOTFILES_CONFIG_LOCAL_DIRECTORY
#     config_remote_repo = DEFAULT_CONFIG_REMOTE_REPO
#
#     config_data = cache_directory.read_from_config()
#
#     config_file_local_directory = config_data.get('local_directory')
#     if config_file_local_directory is not None:
#         config_local_directory = config_file_local_directory
#
#     config_file_remote_repo = config_data.get('remote_repo')
#     if config_file_remote_repo is not None:
#         config_remote_repo = config_file_remote_repo
#
#     return config_local_directory, config_remote_repo
#
#
#
#
#
#
# class ContextualErrorReason:
#     """
#     Nice base wrapper around the tuple struct
#     (ERROR_ENUM, ERROR_CODE, HELP_MESSAGE_FOR_ERROR)
#     """
#
#     def __init__(self, error_enum: Enum, error_code: int, help_message: str):
#         self.error_enum = error_enum
#         self.error_code = error_code
#         self.help_message = help_message
#
#
# class ContextualError(Exception):
#
#     def __init__(self, reason: ContextualErrorReason, help_message_override: Optional[str] = None, context_map: Optional[Dict] = None):
#         super().__init__()
#         self.reason = reason
#         self.help_message_override = help_message_override
#
#         if context_map is None:
#             context_map = {}
#         context_map["help"] = "If you need additional context like a stack trace, please run in verbose mode (with the -v flag)"
#
#         self.context_map = context_map
#
#     @property
#     def help_message(self) -> str:
#         undecorated_original_help_message = self.reason.help_message if self.help_message_override is None else self.help_message_override
#
#         if len(self.context_map) == 0:
#             serialized_context_decoration = ""
#         else:
#             serialized_context_decoration = '\n'.join([f"\t{context_type}: {context_reason}" for context_type, context_reason in self.context_map.items()])
#
#         decorated_error_message = f"{undecorated_original_help_message} [\n{serialized_context_decoration}\n]"
#         return decorated_error_message
#
#     @property
#     def error_enum(self) -> Enum:
#         return self.reason.error_enum
#
#     @property
#     def error_code(self) -> int:
#         return self.reason.error_code
#
#
# class ResponseCode(Enum):
#
#     # General response codes
#     OK_RESPONSE = 0
#
#     # Download response codes
#
#     # Install response codes
#
#     # Uninstall response codes
#
#     # Update response codes
#
#     # Clean response codes
#
#     # Configure response codes
#
#     # Validate response codes
