import pytest

from pydotfiles.defaults import get_current_mac_version
from pydotfiles.defaults import MacVersion


"""
Utility method tests
"""


@pytest.mark.local
def test_get_current_mac_version():
    # System under test
    current_mac_version = get_current_mac_version()

    # Verification
    assert current_mac_version is not None
    assert isinstance(current_mac_version, MacVersion)
