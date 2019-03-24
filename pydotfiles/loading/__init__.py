from pathlib import Path
from json import load as json_load
from yaml import load as yaml_load
from plistlib import load as plist_load
from os import environ

from pydotfiles.service.common import ContextualError
from pydotfiles.service.common import ResponseCode

from typing import Dict, List
from pydotfiles.models.utils import load_data_from_file
from pydotfiles.defaults import MacVersion, VersionRange, Setting

from pydotfiles.environments import VirtualEnvironment
from pydotfiles.environments import LanguagePluginManager, LanguageEnvironmentPluginManager
from pydotfiles.environments import LanguageManager, LanguageEnvironmentManager
from pydotfiles.environments import DevelopmentEnvironment


# def get_pydotfiles_config_data():
#     pass
#
#     def read_from_config(self):
#         if not os.path.isfile(self.config_file):
#             return {}
#
#         with open(self.config_file, 'r') as config_file:
#             return json.load(config_file)
#
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


def get_os_default_settings(default_setting_file_path):
    # Loads in the default settings file
    default_settings_data = load_data_from_file(default_setting_file_path)

    # Parses the default settings data
    return parse_default_settings(default_settings_data)


"""
Loading methods
"""


def load_plist(plist_path):
    with open(plist_path, 'rb') as plist_file:
        return plist_load(plist_file)


def load_config_file(config_file: Path):
    if config_file is None:
        return {}

    config_file_name = str(config_file)
    with config_file.open() as config_fd:
        if config_file_name.endswith(".json"):
            return json_load(config_fd)
        elif config_file_name.endswith(".yaml") or config_file_name.endswith(".yml"):
            return yaml_load(config_fd)
        else:
            raise ContextualError(ResponseCode.UNSUPPORTED_FILE_TYPE, f"Configuration Data Load: The file type of the settings configuration file {config_file} could not be parsed (not a supported filetype)")


"""
Parsing methods
"""


def parse_default_settings(default_settings_data):
    if not default_settings_data:
        default_settings_data = []

    version = default_settings_data.get("version")
    schema_type = default_settings_data.get("schema")

    if version != "alpha":
        raise NotImplementedError(f"Loading: Unable to load default settings file with an unsupported version number [found_version={version}]")

    if schema_type != "default_settings":
        raise ValueError(f"Loading: Invalid data file was passed in based on detected schema type [schema_type={schema_type}]")

    return alpha_default_parse_data(default_settings_data.get("default_settings"))


def parse_developer_environments(developer_environments_data):
    if developer_environments_data is None:
        return []

    return alpha_developer_environments_parse_data(developer_environments_data)


"""
Version-based parsers
"""


def alpha_default_parse_data(default_settings_data):
    settings = []
    for raw_setting in default_settings_data:
        name = raw_setting.get("name")
        enabled = raw_setting.get("enabled", True)
        description = raw_setting.get("description")

        raw_start = raw_setting.get("start")
        start = None if raw_start is None else MacVersion.from_name(raw_start)

        raw_end = raw_setting.get("end")
        end = None if raw_end is None else MacVersion.from_name(raw_end)

        valid_version_range = VersionRange(start, end)
        command = raw_setting.get("command")
        check_command = raw_setting.get("check_command")
        expected_check_state = raw_setting.get("expected_check_state")

        run_as_sudo = raw_setting.get("sudo", False)

        check_output = raw_setting.get("check_output", True)
        settings.append(Setting(
            name=name,
            valid_version_range=valid_version_range,
            command=command,
            enabled=enabled,
            description=description,
            check_command=check_command,
            expected_check_state=expected_check_state,
            run_as_sudo=run_as_sudo,
            check_output=check_output,
        ))

    return settings


def alpha_developer_environments_parse_data(developer_environments_data):
    developer_environments = []

    for raw_developer_environment in developer_environments_data:
        language = raw_developer_environment.get("language")
        versions = raw_developer_environment.get("versions")
        language_environment_manager = parse_language_environment_manager(raw_developer_environment.get("environment_manager"))

        developer_environments.append(DevelopmentEnvironment(
            language=language,
            versions=versions,
            language_environment_manager=language_environment_manager
        ))
    return developer_environments


def parse_language_environment_manager(environment_manager_data: Dict):
    environment_manager = LanguageManager.from_string(environment_manager_data.get("name"))
    plugin_managers = parse_language_environment_plugins(environment_manager_data.get("plugins"))

    return LanguageEnvironmentManager(environment_manager, language_plugin_managers=plugin_managers)


def parse_language_environment_plugins(plugins_data: List[Dict]):
    if plugins_data is None:
        return []

    plugin_managers = []
    for plugin_data in plugins_data:
        language_plugin = LanguagePluginManager.from_string(plugin_data.get("name"))
        virtual_environments_data = parse_virtual_environments(plugin_data.get("virtual_environments"))
        plugin_managers.append(LanguageEnvironmentPluginManager(language_plugin, virtual_environments_data))
    return plugin_managers


def parse_virtual_environments(virtual_environments_data: List[Dict]):
    if virtual_environments_data is None:
        return []
    return [VirtualEnvironment(virtual_environment.get("version"), virtual_environment.get("name")) for virtual_environment in virtual_environments_data]
