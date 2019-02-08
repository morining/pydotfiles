import pytest

from pydotfiles.models.validator import Validator, ConfigMapper
from pydotfiles.models.exceptions import ValidationError
from tests.test_models.validation import load_test_data


"""
ConfigMapper tests
"""


def test_successful_loading_schema_alpha_default_settings():
    # System under test
    schema = ConfigMapper.get_schema("alpha", "default_settings")

    # Verification
    assert schema is not None
    assert schema.get("type") == "object"
    assert schema.get("properties") is not None

    assert schema.get("properties").get("version") is not None
    assert schema.get("properties").get("version").get("enum") is not None
    assert schema.get("properties").get("version").get("enum")[0] is not None
    assert schema.get("properties").get("version").get("enum")[0] == "alpha"

    assert schema.get("properties").get("schema") is not None
    assert schema.get("properties").get("schema").get("enum") is not None
    assert schema.get("properties").get("schema").get("enum")[0] is not None
    assert schema.get("properties").get("schema").get("enum")[1] == "default_settings"


"""
Validator tests
"""


def test_invalid_schema_no_version():
    # Setup
    validator = Validator()
    data = load_test_data("alpha.default_settings", "invalid_schema_no_version.json")

    # System under test
    with pytest.raises(ValidationError):
        validator.validate_data(data)


def test_invalid_schema_no_schema_type():
    # Setup
    validator = Validator()
    data = load_test_data("alpha.default_settings", "invalid_schema_no_schema_type.json")

    # System under test
    with pytest.raises(ValidationError):
        validator.validate_data(data)


def test_invalid_schema_default_settings_no_name():
    # Setup
    validator = Validator()
    data = load_test_data("alpha.default_settings", "invalid_schema_default_settings_no_name.json")

    # System under test
    with pytest.raises(ValidationError):
        validator.validate_data(data)


def test_invalid_schema_default_settings_no_command():
    # Setup
    validator = Validator()
    data = load_test_data("alpha.default_settings", "invalid_schema_default_settings_no_command.json")

    # System under test
    with pytest.raises(ValidationError):
        validator.validate_data(data)


def test_invalid_schema_default_settings_null_start():
    # Setup
    validator = Validator()
    data = load_test_data("alpha.default_settings", "invalid_schema_default_settings_null_start.json")

    # System under test
    with pytest.raises(ValidationError):
        validator.validate_data(data)


def test_invalid_schema_default_settings_null_end():
    # Setup
    validator = Validator()
    data = load_test_data("alpha.default_settings", "invalid_schema_default_settings_null_end.json")

    # System under test
    with pytest.raises(ValidationError):
        validator.validate_data(data)


def test_invalid_schema_default_settings_invalid_start():
    # Setup
    validator = Validator()
    data = load_test_data("alpha.default_settings", "invalid_schema_default_settings_null_start.json")

    # System under test
    with pytest.raises(ValidationError):
        validator.validate_data(data)


def test_invalid_schema_default_settings_invalid_end():
    # Setup
    validator = Validator()
    data = load_test_data("alpha.default_settings", "invalid_schema_default_settings_null_end.json")

    # System under test
    with pytest.raises(ValidationError):
        validator.validate_data(data)


def test_valid_schema_all():
    # Setup
    validator = Validator()
    data = load_test_data("alpha.default_settings", "valid_schema_all.json")

    # System under test
    validator.validate_data(data)
