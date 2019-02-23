import plistlib
import os
import sys
from typing import Dict, List, Set
from pathlib import Path

from pydotfiles.models import Module
from pydotfiles.models.primitives import FileAction
from pydotfiles.models.enums import FileActionType
from pydotfiles.models.utils import load_data_from_file
from pydotfiles.defaults import MacVersion, VersionRange, Setting

from pydotfiles.environments import VirtualEnvironment
from pydotfiles.environments import LanguagePluginManager, LanguageEnvironmentPluginManager
from pydotfiles.environments import LanguageManager, LanguageEnvironmentManager
from pydotfiles.environments import DevelopmentEnvironment

from pydotfiles.common import OS

"""
Helper value structs
"""


class ModuleInformation:

    def __init__(self, modules: List[Module], is_sudo_used: bool):
        self.modules = modules
        self.is_sudo_used = is_sudo_used


class ModulePaths:

    def __init__(self, config_file_paths: Set[Path], script_file_paths: Set[Path], symlink_file_paths: Set[Path], generic_file_paths: Set[Path]):
        self.config_file_paths = config_file_paths
        self.script_file_paths = script_file_paths
        self.symlink_file_paths = symlink_file_paths
        self.generic_file_paths = generic_file_paths

    @property
    def config_paths(self) -> Set[Path]:
        return self.config_paths

    @property
    def script_paths(self) -> Set[Path]:
        return self.script_paths

    @property
    def symlink_paths(self) -> Set[Path]:
        return self.symlink_file_paths

    @property
    def generic_paths(self) -> Set[Path]:
        return self.generic_file_paths


def get_active_modules(config_repo_local, active_modules, cache_directory) -> ModuleInformation:
    host_os = OS.from_string(sys.platform)
    return load_active_modules(config_repo_local, active_modules, host_os, cache_directory)



def get_module_paths(directory: Path) -> ModulePaths:
    # Generates a set of files that we need to validate from a tree structure
    config_file_paths = set()
    script_file_paths = set()
    symlink_file_paths = set()
    generic_file_paths = set()

    for path_prefix, directory_names, file_names in os.walk(directory):
        for file_name_path in file_names:
            file_name = str(file_name_path)
            if file_name.endswith(".json") or file_name.endswith(".yaml") or file_name.endswith(".yml"):
                config_file_paths.add(Path(path_prefix, file_name))
            elif file_name == "start" or file_name == "undo-start" or file_name == "post" or file_name == "undo-post":
                script_file_paths.add(Path(path_prefix, file_name))
            elif file_name.endswith(".symlink"):
                symlink_file_paths.add(Path(path_prefix, file_name))
            else:
                generic_file_paths.add(Path(path_prefix, file_name))

    return ModulePaths(
        config_file_paths=config_file_paths,
        script_file_paths=script_file_paths,
        symlink_file_paths=symlink_file_paths,
        generic_file_paths=generic_file_paths,
    )


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
        return plistlib.load(plist_file)


def get_active_module_paths(config_repo_local, active_modules):
    return get_module_names(config_repo_local) if active_modules is None else active_modules


def load_module(directory: Path) -> Module:
    module_paths = get_module_paths(directory)

    name = get_module_name()
    module_paths

    host_os = OS.from_string(sys.platform)



    # name: str,
    # host_os: str,
    # directory: Path,
    # start_action: FileAction,
    # post_action: FileAction,
    # operating_system: OperatingSystem,
    # developer_environments: List[DevelopmentEnvironment],
    # actions: List[FileAction]


    return Module(
        name=name,
        directory=directory,
        host_os=host_os,
        start_action=start_action,
        post_action=post_action,
        operating_system=operating_system,
        developer_environments=developer_environments,
        actions=actions,

    )



def load_active_modules(config_repo_local, active_modules, host_os, cache_directory):
    modules = {}
    is_sudo_used = False

    module_names = get_active_module_paths(config_repo_local, active_modules)
    for module_name in module_names:
        settings_file = None

        start_file = None
        post_file = None

        undo_start_file = None
        undo_post_file = None

        module_directory = os.path.join(config_repo_local, module_name)
        module_symlinks = []
        module_generic_files = []

        for module_file in os.listdir(module_directory):
            full_module_file_path = os.path.join(module_directory, module_file)
            if module_file == 'start':
                start_file = full_module_file_path
                continue

            if module_file == 'undo-start':
                undo_start_file = full_module_file_path
                continue

            if module_file == 'settings.yaml' or module_file == 'settings.json':
                settings_file = full_module_file_path
                continue

            if module_file == 'post':
                post_file = full_module_file_path
                continue

            if module_file == 'undo-post':
                undo_post_file = full_module_file_path
                continue

            if module_file.endswith(".symlink"):
                module_symlinks.append(full_module_file_path)
            else:
                module_generic_files.append(full_module_file_path)


        """
            def __init__(self, name: str, host_os: str, directory: Path, start_action: FileAction, post_action: FileAction, operating_system: OperatingSystem, developer_environments: List[DevelopmentEnvironment], actions: List[FileAction]):
        self.name = name
        self.directory = directory
        self.host_os = host_os
        self.start_action = start_action
        self.post_action = post_action
        self.operating_system = operating_system
        self.developer_environments = developer_environments
        self.actions = actions
        self.sudo_password = None


 #   ############## TODO KILLAFTER: OLD Logic
        # self.start_action = 
        # self.
        # 
        # # Loads in the settings file
        # self.settings_file = settings_file
        # settings_data = load_data_from_file(self.settings_file)
        # self.operating_system = parse_operating_system_config(settings_data.get('os'), self.cache_directory, self.directory)
        # self.environments = parse_developer_environments(settings_data.get('environments'))
        # self.actions, self.is_sudo_used = parse_action_configs(settings_data.get('actions'), self.directory, self.symlinks, self.other_files)
        # self.sudo_password = None
        """

        start_action = None if start_file is None else FileAction(FileActionType.SCRIPT, start_file, undo_start_file, None, None)
        post_action = None if post_file is None else FileAction(FileActionType.SCRIPT, post_file, undo_post_file, None, None)

        modules[module_name] = Module(
            name=module_name,
            directory=module_directory,
            start_file=start_file,
            post_file=post_file,
            undo_start_file=undo_start_file,
            undo_post_file=undo_post_file,
            settings_file=settings_file,
            symlinks=module_symlinks,
            other_files=module_generic_files,
            host_os=host_os,
            cache_directory=cache_directory
        )

        if modules[module_name].is_sudo_used:
            is_sudo_used = True

    return modules, is_sudo_used


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


"""
Helper methods
"""


def get_module_names(config_repo_local):
    return [module_name for module_name in os.listdir(config_repo_local) if os.path.isdir(os.path.join(config_repo_local, module_name)) and module_name != ".git" and not module_name.startswith(".")]
