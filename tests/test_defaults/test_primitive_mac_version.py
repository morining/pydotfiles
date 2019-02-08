import pytest
from distutils.version import StrictVersion

from pydotfiles.defaults import MacVersion

"""
String name to enum parsing tests
"""


def test_primitive_mac_version_from_valid_name_mojave_string_lowercase():
    # Setup
    version_string = "mojave"

    # System under test
    mac_version = MacVersion.from_name(version_string)

    # Verification
    assert mac_version is not None
    assert isinstance(mac_version, MacVersion)
    assert mac_version == MacVersion.MOJAVE


def test_primitive_mac_version_from_valid_name_mojave_string_uppercase():
    # Setup
    version_string = "MOJAVE"

    # System under test
    mac_version = MacVersion.from_name(version_string)

    # Verification
    assert mac_version is not None
    assert isinstance(mac_version, MacVersion)
    assert mac_version == MacVersion.MOJAVE


def test_primitive_mac_version_from_valid_name_mojave_string_weirdcase():
    # Setup
    version_string = "mOjAvE"

    # System under test
    mac_version = MacVersion.from_name(version_string)

    # Verification
    assert mac_version is not None
    assert isinstance(mac_version, MacVersion)
    assert mac_version == MacVersion.MOJAVE


def test_primitive_mac_version_from_invalid_name_none():
    # Setup
    version_string = None

    # System under test
    with pytest.raises(KeyError):
        MacVersion.from_name(version_string)


def test_primitive_mac_version_from_invalid_name_mavericks_unsupported_version():
    # Setup
    version_string = "mavericks"

    # System under test
    with pytest.raises(KeyError):
        MacVersion.from_name(version_string)


def test_primitive_mac_version_from_invalid_name_mavericks_gibberish():
    # Setup
    version_string = "asdiajodsiajdoaijdoaisjd"

    # System under test
    with pytest.raises(KeyError):
        MacVersion.from_name(version_string)


"""
String version to enum parsing tests
"""


def test_primitive_mac_version_from_valid_version_string_major_minor_patch():
    # Setup
    version_string = "10.13.3"

    # System under test
    mac_version = MacVersion.from_version(version_string)

    # Verification
    assert mac_version is not None
    assert isinstance(mac_version, MacVersion)
    assert mac_version == MacVersion.HIGH_SIERRA


def test_primitive_mac_version_from_valid_version_string_major_minor():
    # Setup
    version_string = "10.13.3"

    # System under test
    mac_version = MacVersion.from_version(version_string)

    # Verification
    assert mac_version is not None
    assert isinstance(mac_version, MacVersion)
    assert mac_version == MacVersion.HIGH_SIERRA


def test_primitive_mac_version_from_invalid_version_string_none():
    # Setup
    version_string = None

    # System under test
    with pytest.raises(ValueError):
        MacVersion.from_version(version_string)


def test_primitive_mac_version_from_invalid_version_string_unsupported_version_major_minor_patch():
    # Setup
    version_string = "10.7.3"

    # System under test
    with pytest.raises(ValueError):
        MacVersion.from_version(version_string)


def test_primitive_mac_version_from_invalid_version_string_unsupported_version_major_minor():
    # Setup
    version_string = "10.7"

    # System under test
    with pytest.raises(ValueError):
        MacVersion.from_version(version_string)


def test_primitive_mac_version_from_invalid_version_string_gibberish():
    # Setup
    version_string = "asdoaijsdoaidjoaidsja"

    # System under test
    with pytest.raises(ValueError):
        MacVersion.from_version(version_string)


"""
StrictVersion to enum parsing tests
"""


def test_primitive_mac_version_from_valid_version_strict_version_major_minor_patch():
    # Setup
    version_string = StrictVersion("10.11")

    # System under test
    mac_version = MacVersion.from_version(version_string)

    # Verification
    assert mac_version is not None
    assert isinstance(mac_version, MacVersion)
    assert mac_version == MacVersion.EL_CAPITAN


def test_primitive_mac_version_from_valid_version_strict_version_major_minor():
    # Setup
    version_string = StrictVersion("10.10")

    # System under test
    mac_version = MacVersion.from_version(version_string)

    # Verification
    assert mac_version is not None
    assert isinstance(mac_version, MacVersion)
    assert mac_version == MacVersion.YOSEMITE


def test_primitive_mac_version_from_invalid_version_strict_unsupported_version_major_minor_patch():
    # Setup
    version_string = StrictVersion("10.5.3")

    # System under test
    with pytest.raises(ValueError):
        MacVersion.from_version(version_string)


def test_primitive_mac_version_from_invalid_version_strict_unsupported_version_major_minor():
    # Setup
    version_string = StrictVersion("10.5")

    # System under test
    with pytest.raises(ValueError):
        MacVersion.from_version(version_string)


"""
Ordering tests
"""


def test_primitive_mac_version_ordering_from_name():
    # Setup
    yosemite = MacVersion.from_name("yosemite")
    high_sierra = MacVersion.from_name("HIGH_SIERRA")
    mojave = MacVersion.from_name("moJaVe")

    correct_sorted_mac_versions = [MacVersion.YOSEMITE, MacVersion.HIGH_SIERRA, MacVersion.MOJAVE]
    unsorted_mac_versions = [high_sierra, mojave, yosemite]

    # System under test
    found_sorted_mac_versions = sorted(unsorted_mac_versions)

    # Verification
    assert correct_sorted_mac_versions == found_sorted_mac_versions


def test_primitive_mac_version_ordering_from_strict():
    # Setup
    yosemite = MacVersion.from_version(StrictVersion("10.10.1"))
    mojave = MacVersion.from_version(StrictVersion("10.14.3"))
    sierra = MacVersion.from_version(StrictVersion("10.12.8"))

    correct_sorted_mac_versions = [MacVersion.YOSEMITE, MacVersion.SIERRA, MacVersion.MOJAVE]
    unsorted_mac_versions = [mojave, sierra, yosemite]

    # System under test
    found_sorted_mac_versions = sorted(unsorted_mac_versions)

    # Verification
    assert correct_sorted_mac_versions == found_sorted_mac_versions


def test_primitive_mac_version_ordering_from_mixed():
    # Setup
    yosemite = MacVersion.from_version(StrictVersion("10.10.1"))
    mojave = MacVersion.from_version("10.14")
    sierra = MacVersion.from_name("sierra")

    correct_sorted_mac_versions = [MacVersion.YOSEMITE, MacVersion.SIERRA, MacVersion.MOJAVE]
    unsorted_mac_versions = [mojave, sierra, yosemite]

    # System under test
    found_sorted_mac_versions = sorted(unsorted_mac_versions)

    # Verification
    assert correct_sorted_mac_versions == found_sorted_mac_versions
