from collections.abc import Generator

import pytest

from src.api.client import ApiClient
from tests.fixtures.config import Config


@pytest.fixture(scope="session")
def api_client(configs: Config) -> Generator[ApiClient, None, None]:
    client = ApiClient(base_url=configs.login_url, api_token=configs.api_token)
    yield client
    client.close()
