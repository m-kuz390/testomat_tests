import httpx
import pytest
from faker import Faker

from src.api.controllers.suite_controller import SuiteController
from src.api.models import Project, Suite

fake = Faker()


def assert_valid_suite(suite: Suite, expected_title: str | None = None) -> None:
    assert isinstance(suite, Suite)
    assert suite.id is not None
    assert suite.type == "suite"
    assert suite.attributes is not None
    if expected_title:
        assert suite.attributes.title == expected_title


@pytest.fixture
def new_suite(suite_controller: SuiteController, project: Project) -> Suite:
    suite = suite_controller.create(project_id=project.id, title=fake.sentence())
    yield suite
    try:
        suite_controller.delete(project_id=project.id, suite_id=suite.id)
    except httpx.HTTPStatusError:
        pass


@pytest.mark.api
def test_create_suite_returns_valid_model(new_suite: Suite):
    assert_valid_suite(new_suite)


@pytest.mark.api
def test_get_suite_by_id_matches_created(
    suite_controller: SuiteController,
    project: Project,
    new_suite: Suite,
):
    fetched = suite_controller.get_by_id(project_id=project.id, suite_id=new_suite.id)

    assert_valid_suite(fetched, expected_title=new_suite.attributes.title)
    assert fetched.id == new_suite.id


# --- Негативні сценарії ---

@pytest.mark.api
def test_create_suite_with_invalid_project_id_returns_404(suite_controller: SuiteController):
    with pytest.raises(httpx.HTTPStatusError) as exc_info:
        suite_controller.create(project_id="non-existent-project", title=fake.sentence())

    assert exc_info.value.response.status_code == 404


@pytest.mark.api
def test_get_suite_with_invalid_id_returns_404(suite_controller: SuiteController, project: Project):
    with pytest.raises(httpx.HTTPStatusError) as exc_info:
        suite_controller.get_by_id(project_id=project.id, suite_id="non-existent-id")

    assert exc_info.value.response.status_code == 404


# --- Update і Delete ---

@pytest.mark.api
def test_update_suite_changes_title(
    suite_controller: SuiteController,
    project: Project,
    new_suite: Suite,
):
    new_title = fake.sentence()

    updated = suite_controller.update(
        project_id=project.id,
        suite_id=new_suite.id,
        title=new_title,
    )

    assert_valid_suite(updated, expected_title=new_title)


@pytest.mark.api
def test_delete_suite_removes_it(suite_controller: SuiteController, project: Project, new_suite: Suite):
    suite_controller.delete(project_id=project.id, suite_id=new_suite.id)

    with pytest.raises(httpx.HTTPStatusError) as exc_info:
        suite_controller.get_by_id(project_id=project.id, suite_id=new_suite.id)

    assert exc_info.value.response.status_code == 404
