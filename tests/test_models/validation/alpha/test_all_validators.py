import json
import pytest

from pydotfiles.models.validator import Validator
from pydotfiles.models.exceptions import ValidationError


def test_both_validators_success(tmpdir):
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


def test_both_validators_fail_invalid_default_settings(tmpdir):
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
