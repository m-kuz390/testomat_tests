import httpx
import pytest
from faker import Faker

from src.api.controllers.suite_controller import SuiteController
from src.api.controllers.test_controller import TestController
from src.api.models import Project, Suite, Test

fake = Faker()


def assert_valid_test(test: Test, expected_title: str | None = None) -> None:
    assert isinstance(test, Test)
    assert test.id is not None
    assert test.type == "test"
    assert test.attributes is not None
    if expected_title:
        assert test.attributes.title == expected_title


@pytest.fixture
def new_suite(suite_controller: SuiteController, project: Project) -> Suite:
    suite = suite_controller.create(project_id=project.id, title=fake.sentence())
    yield suite
    try:
        suite_controller.delete(project_id=project.id, suite_id=suite.id)
    except httpx.HTTPStatusError:
        pass


@pytest.fixture
def new_test(test_controller: TestController, new_suite: Suite, project: Project) -> Test:
    test = test_controller.create(
        project_id=project.id,
        suite_id=new_suite.id,
        title=fake.sentence(),
    )
    yield test
    try:
        test_controller.delete(project_id=project.id, test_id=test.id)
    except httpx.HTTPStatusError:
        pass


@pytest.mark.api
def test_create_test_returns_valid_model(new_test: Test):
    assert_valid_test(new_test)


@pytest.mark.api
def test_get_test_by_id_matches_created(
    test_controller: TestController,
    project: Project,
    new_test: Test,
):
    fetched = test_controller.get_by_id(project_id=project.id, test_id=new_test.id)

    assert_valid_test(fetched, expected_title=new_test.attributes.title)
    assert fetched.id == new_test.id
