from pathlib import Path
from typing import Generator

import pytest
from playwright.sync_api import Browser, BrowserContext, Page

from src.web.application import Application
from tests.fixtures.config import Config
from tests.fixtures.cookie_helper import CookieHelper, clear_browser_state

PROJECT_ROOT = Path(__file__).parents[2]
STORAGE_STATE_PATH = PROJECT_ROOT / "test_result" / ".auth" / "storage_state.json"


def _login_and_save_state(
    browser: Browser,
    browser_context_args: dict,
    configs: Config,
) -> None:
    STORAGE_STATE_PATH.parent.mkdir(parents=True, exist_ok=True)

    ctx = browser.new_context(**browser_context_args)
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


@pytest.fixture(scope="session")
def auth_context(
    browser: Browser,
    browser_context_args: dict,
    storage_state: str,
) -> Generator[BrowserContext, None, None]:
    ctx = browser.new_context(**browser_context_args, storage_state=storage_state)
    yield ctx
    ctx.close()


@pytest.fixture(scope="function")
def app(page: Page) -> Application:
    return Application(page)


@pytest.fixture(scope="function")
def cookies(page: Page) -> CookieHelper:
    return CookieHelper(page.context)


@pytest.fixture(scope="function")
def logged_app(auth_context: BrowserContext) -> Generator[Application, None, None]:
    pg = auth_context.new_page()
    pg.goto("/projects")
    yield Application(pg)
    pg.close()


@pytest.fixture(scope="module")
def module_context(
    browser: Browser,
    browser_context_args: dict,
) -> Generator[BrowserContext, None, None]:
    ctx = browser.new_context(**browser_context_args)
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
