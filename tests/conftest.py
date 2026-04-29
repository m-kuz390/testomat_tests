from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent

pytest_plugins = [
    "tests.fixtures.config",
    "tests.fixtures.playwright",
    "tests.fixtures.cookie_helper",
    "tests.fixtures.app",
]


def pytest_configure(config):
    config.option.htmlpath = str(PROJECT_ROOT / "test_result" / "report.html")
