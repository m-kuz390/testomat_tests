import os
from dataclasses import dataclass

import pytest
from dotenv import load_dotenv

from src.web.Application import Application

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
def app(page) -> Application:
    return Application(page)


@pytest.fixture(scope="function")
def login(app: Application, configs: Config):
    app.login_page.open()
    app.login_page.is_loaded()
    app.login_page.login(email=configs.email, password=configs.password)
