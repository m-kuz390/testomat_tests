import pytest

from src.api.client import ApiClient


@pytest.mark.api
def test_response_is_successful(api_client: ApiClient):
    response = api_client.get("/api/projects")

    assert response.status_code == 200


@pytest.mark.api
def test_response_contains_projects_data(api_client: ApiClient):
    body = api_client.get("/api/projects").json()

    assert "data" in body
    assert isinstance(body["data"], list)


@pytest.mark.api
def test_each_project_has_id_and_type(api_client: ApiClient):
    projects = api_client.get("/api/projects").json()["data"]

    for project in projects:
        assert "id" in project
        assert "type" in project


@pytest.mark.api
def test_each_project_has_title_in_attributes(api_client: ApiClient):
    projects = api_client.get("/api/projects").json()["data"]

    for project in projects:
        title = project["attributes"]["title"]
        assert title and isinstance(title, str)
