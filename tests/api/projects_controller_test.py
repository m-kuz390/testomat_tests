import httpx
import pytest

from src.api.controllers.project_controller import ProjectController
from src.api.models import Project


def assert_valid_project(project: Project) -> None:
    assert isinstance(project, Project)
    assert project.id is not None
    assert project.type == "project"
    assert project.attributes is not None
    assert project.attributes.title is not None


@pytest.mark.smoke
@pytest.mark.api
def test_get_all_projects_returns_valid_models(project_controller: ProjectController):
    projects = project_controller.get_all()

    assert len(projects) > 0
    for project in projects:
        assert_valid_project(project)


@pytest.mark.regression
@pytest.mark.api
def test_get_project_by_id_matches(project_controller: ProjectController, project: Project):
    fetched = project_controller.get_by_id(project_id=project.id)

    assert_valid_project(fetched)
    assert fetched.id == project.id
    assert fetched.attributes.title == project.attributes.title


@pytest.mark.regression
@pytest.mark.api
def test_get_project_with_invalid_id_returns_404(project_controller: ProjectController):
    with pytest.raises(httpx.HTTPStatusError) as exc_info:
        project_controller.get_by_id(project_id="non-existent-project")

    assert exc_info.value.response.status_code == 404
