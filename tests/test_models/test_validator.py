import pytest
import json
import yaml
import uuid
from pkg_resources import resource_stream

from pydotfiles.models.validator import Validator, ConfigMapper
from pydotfiles.models.exceptions import ValidationError

"""
ConfigMapper tests
"""


def test_successful_loading_schema_alpha():
    # System under test
    schema = ConfigMapper.get_schema("alpha")

    # Verification
    assert schema is not None
    assert schema.get("type") == "object"
    assert schema.get("properties") is not None
    assert schema.get("properties").get("version") is not None
    assert schema.get("properties").get("version").get("enum") is not None
    assert schema.get("properties").get("version").get("enum")[0] is not None
    assert schema.get("properties").get("version").get("enum")[0] == "alpha"


"""
Validator tests
"""


def test_invalid_directory_none():
    # Setup
    validator = Validator()

    # System under test
    with pytest.raises(ValidationError):
        validator.validate_directory(None)


def test_invalid_directory_name():
    # Setup
    validator = Validator()
    invalid_directory_name = str(uuid.uuid4())

    # System under test
    with pytest.raises(ValidationError):
        validator.validate_directory(invalid_directory_name)


def test_valid_directory(tmpdir):
    # Setup
    validator = Validator()
    valid_file = tmpdir.join("settings.json")
    valid_file_content = "{\"version\": \"alpha\"}"
    valid_file.write(valid_file_content)

    # System under test
    validator.validate_directory(tmpdir.strpath)


def test_valid_directory_multiple_modules(tmpdir):
    # Setup
    validator = Validator()
    modules_settings_file_a = tmpdir.mkdir("a_directory").join("settings.json")
    modules_settings_file_a_content = "{\"version\": \"alpha\"}"
    modules_settings_file_a.write(modules_settings_file_a_content)

    modules_settings_file_b = tmpdir.mkdir("b_directory").join("settings.yaml")
    modules_settings_file_b_content = "version: \"alpha\""
    modules_settings_file_b.write(modules_settings_file_b_content)

    # System under test
    validator.validate_directory(tmpdir.strpath)


def test_invalid_file_none():
    # Setup
    validator = Validator()

    # System under test
    with pytest.raises(ValidationError):
        validator.validate_file(None)


def test_invalid_file_name():
    # Setup
    validator = Validator()
    invalid_file_name = str(uuid.uuid4())

    # System under test
    with pytest.raises(ValidationError):
        validator.validate_file(invalid_file_name)


def test_invalid_file_empty_file(tmpdir):
    # Setup
    validator = Validator()
    invalid_file = tmpdir.join("invalid_json.json")
    invalid_file_content = ""
    invalid_file.write(invalid_file_content)

    # System under test
    with pytest.raises(ValidationError):
        validator.validate_file(invalid_file.strpath)


def test_invalid_file_invalid_json(tmpdir):
    # Setup
    validator = Validator()
    invalid_file = tmpdir.join("invalid_json.json")
    invalid_file_content = "{\"version\": \"alpha,}"
    invalid_file.write(invalid_file_content)

    # System under test
    with pytest.raises(ValidationError):
        validator.validate_file(invalid_file.strpath)


def test_valid_file(tmpdir):
    # Setup
    validator = Validator()
    valid_file = tmpdir.join("valid_json.json")
    valid_file_content = "{\"version\": \"alpha\"}"
    valid_file.write(valid_file_content)

    # System under test
    validator.validate_file(valid_file.strpath)


def test_invalid_data_none():
    # Setup
    validator = Validator()

    # System under test
    with pytest.raises(ValidationError):
        validator.validate_data(None)


def test_invalid_schema_no_version():
    # Setup
    validator = Validator()
    data = load_test_data("invalid_schema_no_version.json")

    # System under test
    with pytest.raises(ValidationError):
        validator.validate_data(data)


def test_invalid_schema_action_no_action():
    # Setup
    validator = Validator()
    data = load_test_data("invalid_schema_actions_no_action.json")

    # System under test
    with pytest.raises(ValidationError):
        validator.validate_data(data)


def test_invalid_schema_action_no_files():
    # Setup
    validator = Validator()
    data = load_test_data("invalid_schema_actions_no_files.json")

    # System under test
    with pytest.raises(ValidationError):
        validator.validate_data(data)


def test_invalid_schema_action_invalid_action():
    # Setup
    validator = Validator()
    data = load_test_data("invalid_schema_actions_invalid_action.json")

    # System under test
    with pytest.raises(ValidationError):
        validator.validate_data(data)


def test_invalid_schema_environments_no_name():
    # Setup
    validator = Validator()
    data = load_test_data("invalid_schema_environments_no_name.json")

    # System under test
    with pytest.raises(ValidationError):
        validator.validate_data(data)


def test_invalid_schema_environments_invalid_name():
    # Setup
    validator = Validator()
    data = load_test_data("invalid_schema_environments_invalid_name.json")

    # System under test
    with pytest.raises(ValidationError):
        validator.validate_data(data)


def test_invalid_schema_os_no_name():
    # Setup
    validator = Validator()
    data = load_test_data("invalid_schema_os_no_name.json")

    # System under test
    with pytest.raises(ValidationError):
        validator.validate_data(data)


def test_invalid_schema_os_invalid_name():
    # Setup
    validator = Validator()
    data = load_test_data("invalid_schema_os_invalid_name.json")

    # System under test
    with pytest.raises(ValidationError):
        validator.validate_data(data)


def test_valid_schema_actions():
    # Setup
    validator = Validator()
    data = load_test_data("valid_schema_actions.json")

    # System under test
    validator.validate_data(data)


def test_valid_schema_os():
    # Setup
    validator = Validator()
    data = load_test_data("valid_schema_os.json")

    # System under test
    validator.validate_data(data)


def test_valid_schema_environments():
    # Setup
    validator = Validator()
    data = load_test_data("valid_schema_environments.json")

    # System under test
    validator.validate_data(data)


def test_valid_schema_all():
    # Setup
    validator = Validator()
    data = load_test_data("valid_schema_all.json")

    # System under test
    validator.validate_data(data)


"""
Helper functions
"""


def load_test_data(file_name):
    if file_name.endswith(".json"):
        return json.load(resource_stream('tests.resources.validator', file_name))
    elif file_name.endswith(".yaml") or file_name.endswith(".yml"):
        return yaml.load(resource_stream('tests.resources.validator', file_name))
