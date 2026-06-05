from collections.abc import Generator

import httpx
import pytest

from src.api.client import ApiClient
from src.api.controllers import ProjectController, SuiteController, TestController
from src.api.models import Project
from tests.fixtures.config import Config


@pytest.fixture(scope="session")
def api_client(configs: Config) -> Generator[ApiClient, None, None]:
    client = ApiClient(base_url=configs.login_url, api_token=configs.api_token)
    yield client
    client.close()


@pytest.fixture(scope="session")
def auth_token(configs: Config) -> str:
    with httpx.Client(base_url=configs.login_url) as client:
        response = client.post("/api/login", json={"api_token": configs.api_token})
        response.raise_for_status()
        return response.json()["jwt"]


@pytest.fixture(scope="session")
def project_controller(configs: Config, auth_token: str) -> Generator[ProjectController, None, None]:
    controller = ProjectController(
        base_url=configs.login_url,
        api_token=configs.api_token,
        jwt_token=auth_token,
    )
    yield controller
    controller.close()


@pytest.fixture(scope="session")
def suite_controller(configs: Config, auth_token: str) -> Generator[SuiteController, None, None]:
    controller = SuiteController(
        base_url=configs.login_url,
        api_token=configs.api_token,
        jwt_token=auth_token,
    )
    yield controller
    controller.close()


@pytest.fixture(scope="session")
def test_controller(configs: Config, auth_token: str) -> Generator[TestController, None, None]:
    controller = TestController(
        base_url=configs.login_url,
        api_token=configs.api_token,
        jwt_token=auth_token,
    )
    yield controller
    controller.close()


@pytest.fixture(scope="function")
def project(project_controller: ProjectController) -> Project:
    """Get the first available project as a precondition."""
    return project_controller.get_all()[0]
