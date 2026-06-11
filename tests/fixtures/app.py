import os
from pathlib import Path
from typing import Generator

import pytest
from playwright.sync_api import Browser, BrowserContext, Page, expect

from src.web.application import Application
from tests.fixtures.config import Config
from tests.fixtures.cookie_helper import CookieHelper, clear_browser_state
from tests.fixtures.playwright import start_tracing, stop_tracing_on_failure

PROJECT_ROOT = Path(__file__).parents[2]
TEST_RESULT_DIR = PROJECT_ROOT / "test_result"
STORAGE_STATE_PATH = TEST_RESULT_DIR / ".auth" / "storage_state.json"


def _make_context(
    browser: Browser,
    browser_context_args: dict,
    storage_path: Path | None = None,
) -> BrowserContext:
    kwargs = {**browser_context_args}

    if os.getenv("CI", "false").lower() != "true":
        kwargs["record_video_dir"] = str(TEST_RESULT_DIR / "videos")

    has_state = storage_path is not None and storage_path.exists()
    if has_state:
        kwargs["storage_state"] = str(storage_path)

    return browser.new_context(**kwargs)


def _login_and_save_state(
    browser: Browser,
    browser_context_args: dict,
    configs: Config,
) -> None:
    STORAGE_STATE_PATH.parent.mkdir(parents=True, exist_ok=True)

    ctx = _make_context(browser, browser_context_args)
    pg = ctx.new_page()
    _app = Application(pg)
    _app.home_page.open()
    _app.home_page.is_loaded()
    _app.home_page.click_login()
    _app.login_page.is_loaded()
    _app.login_page.login_user(configs.email, configs.password)

    ctx.storage_state(path=str(STORAGE_STATE_PATH))
    ctx.close()


@pytest.fixture(scope="session")
def storage_state(
    browser: Browser,
    browser_context_args: dict,
    configs: Config,
) -> str:
    if not STORAGE_STATE_PATH.exists():
        _login_and_save_state(browser, browser_context_args, configs)
    return str(STORAGE_STATE_PATH)


@pytest.fixture(scope="function")
def app(page: Page) -> Application:
    return Application(page)


@pytest.fixture(scope="function")
def cookies(page: Page) -> CookieHelper:
    return CookieHelper(page.context)


@pytest.fixture(scope="function")
def logged_cookies(logged_app: Application) -> CookieHelper:
    return CookieHelper(logged_app.page.context)


@pytest.fixture(scope="function")
def logged_app(
    browser: Browser,
    browser_context_args: dict,
    storage_state: str,
    request: pytest.FixtureRequest,
) -> Generator[Application, None, None]:
    ctx = _make_context(browser, browser_context_args, STORAGE_STATE_PATH)
    start_tracing(ctx)
    pg = ctx.new_page()
    pg.goto("/projects")
    yield Application(pg)
    stop_tracing_on_failure(pg, request)
    pg.close()
    ctx.close()


@pytest.fixture(scope="module")
def module_context(
    browser: Browser,
    browser_context_args: dict,
) -> Generator[BrowserContext, None, None]:
    ctx = _make_context(browser, browser_context_args)
    yield ctx
    ctx.close()


@pytest.fixture(scope="module")
def module_page(module_context: BrowserContext) -> Generator[Page, None, None]:
    pg = module_context.new_page()
    yield pg
    pg.close()


@pytest.fixture(scope="function")
def shared_app(module_page: Page) -> Generator[Application, None, None]:
    yield Application(module_page)
    clear_browser_state(module_page)


@pytest.fixture(scope="function")
def login(app: Application, configs: Config):
    app.login_page.open()
    app.login_page.is_loaded()
    app.login_page.login_user(email=configs.email, password=configs.password)


@pytest.fixture(scope="function")
def free_project_app(
    browser: Browser,
    browser_context_args: dict,
    storage_state: str,
    request: pytest.FixtureRequest,
) -> Generator[Application, None, None]:
    ctx = _make_context(browser, browser_context_args, STORAGE_STATE_PATH)
    start_tracing(ctx)
    pg = ctx.new_page()
    pg.goto("/projects")
    app = Application(pg)
    app.projects_page.is_loaded()
    app.projects_page.header.select_company("Free Projects")
    expect(app.projects_page.header.free_plan_label).to_be_visible()
    yield app
    stop_tracing_on_failure(pg, request)
    pg.close()
    ctx.close()
