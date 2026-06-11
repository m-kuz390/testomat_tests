import time
from pathlib import Path
from typing import Generator, cast

import pytest
from pluggy import Result

PROJECT_ROOT = Path(__file__).parent.parent
_RETENTION_SECONDS = 14 * 24 * 60 * 60

pytest_plugins = [
    "tests.fixtures.config",
    "tests.fixtures.playwright",
    "tests.fixtures.cookie_helper",
    "tests.fixtures.app",
    "tests.fixtures.api",
    "tests.fixtures.selenium",
]


def pytest_sessionstart(session: pytest.Session) -> None:  # noqa: ARG001
    cutoff = time.time() - _RETENTION_SECONDS
    for folder in ["traces", "videos"]:
        directory = PROJECT_ROOT / "test_result" / folder
        if not directory.exists():
            continue
        for file in directory.iterdir():
            if file.is_file() and file.stat().st_mtime < cutoff:
                file.unlink()


def pytest_configure(config):
    config.option.htmlpath = str(PROJECT_ROOT / "test_result" / "report.html")


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item: pytest.Item, call: pytest.CallInfo) -> Generator:  # noqa: ARG001
    outcome = cast(Result, cast(object, (yield)))
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)
