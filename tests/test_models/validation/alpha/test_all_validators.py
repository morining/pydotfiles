import json
import pytest

from pydotfiles.models.validator import Validator
from pydotfiles.models.exceptions import ValidationError


def test_all_validators_success(tmpdir):
    # Setup
    validator = Validator()

    valid_default_settings_file_name = "some-default-settings-file.json"

    valid_core_path = tmpdir.join("settings.json")
    valid_core_file_content = {
        'version': 'alpha',
        'schema': 'core',
        'os': {
            'name': 'macos',
            'default_settings_file': valid_default_settings_file_name
        }
    }
    valid_core_path.write(json.dumps(valid_core_file_content))

    valid_default_settings_path = tmpdir.join(valid_default_settings_file_name)
    valid_default_settings_content = {
        'version': 'alpha',
        'schema': 'default_settings',
        'default_settings': [
            {
                'name': 'some valid minimal example',
                'command': 'echo "some valid minimal example command"'
            }
        ]
    }
    valid_default_settings_path.write(json.dumps(valid_default_settings_content))

    valid_developer_environments_file_name = "some-default-settings-file.json"

    valid_developer_environments_path = tmpdir.join("settings.json")
    valid_developer_environments_file_content = {
        "version": "alpha",
        "schema": "developer_environments",
        "environments": [
            {
                "language": "python",
                "versions": ["3.7.2", "3.6.8"]
            },
            {
                "language": "python",
                "versions": ["3.7.2", "3.6.8"]
            }
        ]
    }
    valid_developer_environments_path.write(json.dumps(valid_developer_environments_file_content))

    # System under test
    validator.validate_directory(tmpdir.strpath)


def test_core_and_default_settings_validators_success(tmpdir):
    # Setup
    validator = Validator()

    valid_default_settings_file_name = "some-default-settings-file.json"

    valid_core_path = tmpdir.join("settings.json")
    valid_core_file_content = {
        'version': 'alpha',
        'schema': 'core',
        'os': {
            'name': 'macos',
            'default_settings_file': valid_default_settings_file_name
        }
    }
    valid_core_path.write(json.dumps(valid_core_file_content))

    valid_default_settings_path = tmpdir.join(valid_default_settings_file_name)
    valid_default_settings_content = {
        'version': 'alpha',
        'schema': 'default_settings',
        'default_settings': [
            {
                'name': 'some valid minimal example',
                'command': 'echo "some valid minimal example command"'
            }
        ]
    }
    valid_default_settings_path.write(json.dumps(valid_default_settings_content))

    # System under test
    validator.validate_directory(tmpdir.strpath)


def test_core_and_default_settings_validators_fail_invalid_default_settings(tmpdir):
    # Setup
    validator = Validator()

    invalid_default_settings_file_name = "some-default-settings-file.json"

    valid_core_path = tmpdir.join("settings.json")
    valid_core_file_content = {
        'version': 'alpha',
        'schema': 'core',
        'os': {
            'name': 'macos',
            'default_settings_file': invalid_default_settings_file_name
        }
    }
    valid_core_path.write(json.dumps(valid_core_file_content))

    invalid_default_settings_path = tmpdir.join(invalid_default_settings_file_name)
    invalid_default_settings_content = {
        'version': 'alpha',
        'schema': 'default_settings',
        'default_settings': [
            {
                'name': 'some valid minimal example',
                'command': 'echo "some valid minimal example command"',
                'start': 'some invalid start mac version'
            }
        ]
    }
    invalid_default_settings_path.write(json.dumps(invalid_default_settings_content))

    # System under test
    with pytest.raises(ValidationError):
        validator.validate_directory(tmpdir.strpath)


def test_all_validators_fail_invalid_developer_environment_version_type(tmpdir):
    # Setup
    validator = Validator()

    valid_default_settings_file_name = "some-default-settings-file.json"

    valid_core_path = tmpdir.join("settings.json")
    valid_core_file_content = {
        'version': 'alpha',
        'schema': 'core',
        'os': {
            'name': 'macos',
            'default_settings_file': valid_default_settings_file_name
        }
    }
    valid_core_path.write(json.dumps(valid_core_file_content))

    valid_default_settings_path = tmpdir.join(valid_default_settings_file_name)
    valid_default_settings_content = {
        'version': 'alpha',
        'schema': 'default_settings',
        'default_settings': [
            {
                'name': 'some valid minimal example',
                'command': 'echo "some valid minimal example command"'
            }
        ]
    }
    valid_default_settings_path.write(json.dumps(valid_default_settings_content))

    valid_developer_environments_file_name = "some-default-settings-file.json"

    valid_developer_environments_path = tmpdir.join("settings.json")
    valid_developer_environments_file_content = {
        "version": "alpha",
        "schema": "developer_environments",
        "environments": [
            {
                "language": 1,
                "versions": ["3.7.2", "3.6.8"]
            },
            {
                "language": "python",
                "versions": ["3.7.2", "3.6.8"]
            }
        ]
    }
    valid_developer_environments_path.write(json.dumps(valid_developer_environments_file_content))

    # System under test
    with pytest.raises(ValidationError):
        validator.validate_directory(tmpdir.strpath)
