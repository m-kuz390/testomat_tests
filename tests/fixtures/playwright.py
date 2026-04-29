from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).parents[2]


@pytest.fixture(scope="session")
def browser_type_launch_args(browser_type_launch_args: dict) -> dict:
    return {
        **browser_type_launch_args,
        "channel": "chrome",
        "headless": False,
        "slow_mo": 0,
        "timeout": 30000,
    }


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args: dict) -> dict:
    return {
        **browser_context_args,
        "base_url": "https://app.testomat.io",
        "viewport": None,
        "locale": "uk-UA",
        "timezone_id": "Europe/Kyiv",
        "record_video_dir": str(PROJECT_ROOT / "test_result" / "videos"),
        "permissions": ["geolocation"],
    }
