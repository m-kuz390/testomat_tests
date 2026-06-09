import os
from pathlib import Path
from typing import Generator

import pytest
from playwright.sync_api import Browser, BrowserContext

IS_CI = bool(os.getenv("CI"))

PROJECT_ROOT = Path(__file__).parents[2]
TRACES_DIR = PROJECT_ROOT / "test_result" / "traces"


def start_tracing(context: BrowserContext) -> None:
    context.tracing.start(screenshots=True, snapshots=True, sources=True)


def stop_tracing_on_failure(context: BrowserContext, request: pytest.FixtureRequest) -> None:
    failed = hasattr(request.node, "rep_call") and request.node.rep_call.failed
    if failed:
        trace_path = TRACES_DIR / f"{request.node.name}.zip"
        trace_path.parent.mkdir(parents=True, exist_ok=True)
        context.tracing.stop(path=trace_path)
    else:
        context.tracing.stop()


@pytest.fixture(scope="session")
def browser_type_launch_args(browser_type_launch_args: dict) -> dict:
    args = {
        **browser_type_launch_args,
        "headless": IS_CI,
        "slow_mo": 0,
        "timeout": 30000,
    }
    if not IS_CI:
        args["channel"] = "chrome"
    return args


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args: dict) -> dict:
    return {
        **browser_context_args,
        "base_url": "https://app.testomat.io",
        "viewport": None,
        "locale": "uk-UA",
        "timezone_id": "Europe/Kyiv",
        "permissions": ["geolocation"],
    }


@pytest.fixture(scope="function")
def context(
    browser: Browser,
    browser_context_args: dict,
    request: pytest.FixtureRequest,
) -> Generator[BrowserContext, None, None]:
    ctx = browser.new_context(**browser_context_args)
    start_tracing(ctx)
    yield ctx
    stop_tracing_on_failure(ctx, request)
    ctx.close()
