from pathlib import Path
from typing import Generator, cast

import pytest
from pluggy import Result

PROJECT_ROOT = Path(__file__).parent.parent

pytest_plugins = [
    "tests.fixtures.config",
    "tests.fixtures.playwright",
    "tests.fixtures.cookie_helper",
    "tests.fixtures.app",
    "tests.fixtures.api",
    "tests.fixtures.selenium",
]


def pytest_configure(config):
    config.option.htmlpath = str(PROJECT_ROOT / "test_result" / "report.html")


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item: pytest.Item, call: pytest.CallInfo) -> Generator:  # noqa: ARG001
    outcome = cast(Result, cast(object, (yield)))
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)
