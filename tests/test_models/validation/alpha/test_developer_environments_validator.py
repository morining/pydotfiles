import pytest

from pydotfiles.models.validator import Validator, ConfigMapper
from pydotfiles.models.exceptions import ValidationError
from tests.test_models.validation import load_test_data


"""
ConfigMapper tests
"""


def test_successful_loading_schema_alpha_developer_environments():
    # System under test
    schema = ConfigMapper.get_schema("alpha", "developer_environments")

    # Verification
    assert schema is not None
    assert schema.get("type") == "object"

    assert schema.get("allOf") is not None
    assert len(schema.get("allOf")) == 2

    assert schema.get("allOf")[0] is not None
    assert schema.get("allOf")[0].get("$ref") is not None
    assert schema.get("allOf")[0].get("$ref") == "./common.json"

    assert schema.get("allOf")[1] is not None
    assert schema.get("allOf")[1].get("properties") is not None

    assert schema.get("allOf")[1].get("properties").get("environments") is not None


"""
Validator tests
"""


def test_invalid_schema_no_version():
    # Setup
    validator = Validator()
    data = load_test_data("alpha.developer_environments", "invalid_schema_no_version.json")

    # System under test
    with pytest.raises(ValidationError):
        validator.validate_data(data)


def test_invalid_schema_no_schema_type():
    # Setup
    validator = Validator()
    data = load_test_data("alpha.developer_environments", "invalid_schema_no_schema_type.json")

    # System under test
    with pytest.raises(ValidationError):
        validator.validate_data(data)


def test_invalid_schema_environments_no_language():
    # Setup
    validator = Validator()
    data = load_test_data("alpha.developer_environments", "invalid_schema_environments_no_language.json")

    # System under test
    with pytest.raises(ValidationError):
        validator.validate_data(data)


def test_invalid_schema_environments_no_versions():
    # Setup
    validator = Validator()
    data = load_test_data("alpha.developer_environments", "invalid_schema_environments_no_versions.json")

    # System under test
    with pytest.raises(ValidationError):
        validator.validate_data(data)


def test_invalid_schema_environments_manager_no_name():
    # Setup
    validator = Validator()
    data = load_test_data("alpha.developer_environments", "invalid_schema_environment_manager_no_name.json")

    # System under test
    with pytest.raises(ValidationError):
        validator.validate_data(data)


def test_invalid_schema_plugin_no_name():
    # Setup
    validator = Validator()
    data = load_test_data("alpha.developer_environments", "invalid_schema_plugin_no_name.json")

    # System under test
    with pytest.raises(ValidationError):
        validator.validate_data(data)


def test_invalid_schema_virtual_environments_no_name():
    # Setup
    validator = Validator()
    data = load_test_data("alpha.developer_environments", "invalid_schema_virtual_environments_no_name.json")

    # System under test
    with pytest.raises(ValidationError):
        validator.validate_data(data)


def test_invalid_schema_virtual_environments_no_version():
    # Setup
    validator = Validator()
    data = load_test_data("alpha.developer_environments", "invalid_schema_virtual_environments_no_version.json")

    # System under test
    with pytest.raises(ValidationError):
        validator.validate_data(data)


def test_valid_schema_all():
    # Setup
    validator = Validator()
    data = load_test_data("alpha.developer_environments", "valid_schema_all.json")

    # System under test
    validator.validate_data(data)
