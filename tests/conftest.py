import os
from dataclasses import dataclass
from typing import Generator

import pytest
from dotenv import load_dotenv
from playwright.sync_api import Browser, BrowserContext, Page

from src.web.application import Application

load_dotenv()


@dataclass(frozen=True)
class Config:
    base_url: str
    login_url: str
    email: str
    password: str


@pytest.fixture(scope="session")
def configs():
    return Config(
        base_url=os.getenv('BASE_URL'),
        login_url=os.getenv('BASE_APP_URL'),
        email=os.getenv('EMAIL'),
        password=os.getenv('PASSWORD')
    )


@pytest.fixture(scope="function")
def app(page: Page) -> Application:
    return Application(page)


@pytest.fixture(scope="session")
def auth_context(browser: Browser, browser_context_args: dict, configs: Config) -> Generator[
    BrowserContext, None, None]:
    ctx = browser.new_context(**browser_context_args)
    pg = ctx.new_page()
    _app = Application(pg)
    _app.home_page.open()
    _app.home_page.is_loaded()
    _app.home_page.click_login()
    _app.login_page.is_loaded()
    _app.login_page.login_user(configs.email, configs.password)
    yield ctx
    ctx.close()


@pytest.fixture(scope="function")
def logged_app(auth_context: BrowserContext) -> Generator[Application, None, None]:
    pg = auth_context.new_page()
    pg.goto("/projects")
    yield Application(pg)
    pg.close()


def clear_browser_state(page: Page) -> None:
    page.context.clear_cookies()
    page.evaluate("() => { localStorage.clear(); sessionStorage.clear(); }")


@pytest.fixture(scope="module")
def module_context(browser: Browser, browser_context_args: dict) -> Generator[BrowserContext, None, None]:
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


@pytest.fixture(scope="session")
def browser_type_launch_args(browser_type_launch_args: dict) -> dict:
    return {
        **browser_type_launch_args,
        "channel": "chrome",
        "headless": False,
        "slow_mo": 0,
        "timeout": 30000
    }


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args: dict) -> dict:
    return {
        **browser_context_args,
        "base_url": "https://app.testomat.io",
        "viewport": None,
        "locale": "uk-UA",
        "timezone_id": "Europe/Kyiv",
        "record_video_dir": "videos/",
        "permissions": ["geolocation"],
    }
