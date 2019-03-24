# General imports
from typing import List

# Vendor imports
from pytest import mark
from _pytest.config import Config


def pytest_addoption(parser):
    parser.addoption("--runslow", action="store_true", default=False, help="Runs slow tests")
    parser.addoption("--run-integration-tests", action="store_true", default=False, help="Runs slower integration tests that do real IO/network calls")
    parser.addoption("--run-end-to-end-tests", action="store_true", default=False, help="Runs extremely slow end-to-end tests that do real IO/network calls")


def pytest_collection_modifyitems(config: Config, items: List):
    if not config.getoption("--runslow"):
        # --runslow not given in the cli: skip slow tests
        skip_slow = mark.skip(reason="need --runslow option to run")
        for item in items:
            if "slow" in item.keywords:
                item.add_marker(skip_slow)

    if not config.getoption("--run-integration-tests"):
        # --run-integration-tests not given in the cli: skip integration tests
        skip_integration = mark.skip(reason="need --run-integration-tests option to run")
        for item in items:
            if "integration" in item.keywords:
                item.add_marker(skip_integration)

    if not config.getoption("--run-end-to-end-tests"):
        # --run-end-to-end-tests not given in the cli: skip end-to-end tests
        skip_integration = mark.skip(reason="need --run-end-to-end-tests option to run")
        for item in items:
            if "etoe" in item.keywords:
                item.add_marker(skip_integration)
