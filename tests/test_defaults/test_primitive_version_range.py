import pytest
from distutils.version import StrictVersion, LooseVersion

from pydotfiles.defaults import VersionRange


"""
Primitive tests
"""


def test_primitive_version_range_from_all_none():
    # System under test
    version_range = VersionRange()

    # Verification
    assert version_range is not None

    really_new_version_number = StrictVersion("100.100")
    assert version_range.is_in_range(really_new_version_number)

    really_old_version_number = StrictVersion("3.0")
    assert version_range.is_in_range(really_old_version_number)


def test_primitive_version_range_from_none_start():
    # Setup
    end_version_number = StrictVersion("10.15")

    # System under test
    version_range = VersionRange(end=end_version_number)

    # Verification
    assert version_range is not None

    really_new_version_number = StrictVersion("100.100")
    assert not version_range.is_in_range(really_new_version_number)

    really_old_version_number = StrictVersion("3.0")
    assert version_range.is_in_range(really_old_version_number)


def test_primitive_version_range_from_none_end():
    # Setup
    start_version_number = StrictVersion("10.12")

    # System under test
    version_range = VersionRange(start=start_version_number)

    # Verification
    assert version_range is not None

    really_new_version_number = StrictVersion("100.100")
    assert version_range.is_in_range(really_new_version_number)

    really_old_version_number = StrictVersion("3.0")
    assert not version_range.is_in_range(really_old_version_number)


def test_primitive_version_range_from_valid_start_and_ends():
    # Setup
    start_version_number = StrictVersion("10.12")
    end_version_number = StrictVersion("10.15")

    # System under test
    version_range = VersionRange(start_version_number, end_version_number)

    # Verification
    assert version_range is not None

    really_new_version_number = StrictVersion("100.100")
    assert not version_range.is_in_range(really_new_version_number)

    really_old_version_number = StrictVersion("3.0")
    assert not version_range.is_in_range(really_old_version_number)

    valid_in_between_version_number = StrictVersion("10.13")
    assert version_range.is_in_range(valid_in_between_version_number)

    valid_end_edge_version_number = StrictVersion("10.15")
    assert version_range.is_in_range(valid_end_edge_version_number)

    valid_start_edge_version_number = StrictVersion("10.12")
    assert version_range.is_in_range(valid_start_edge_version_number)


def test_primitive_version_range_from_invalid_type_string_start():
    # System under test
    with pytest.raises(ValueError):
        VersionRange(start="10.12")


def test_primitive_version_range_from_invalid_type_string_end():
    # System under test
    with pytest.raises(ValueError):
        VersionRange(end="10.15")


def test_primitive_version_range_from_invalid_type_string_both():
    # System under test
    with pytest.raises(ValueError):
        VersionRange(start="10.12", end="10.15")


def test_primitive_version_range_from_invalid_loose_version():
    # Setup
    some_loose_version = LooseVersion("10.12")

    # System under test
    with pytest.raises(ValueError):
        VersionRange(some_loose_version)
