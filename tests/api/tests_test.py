import httpx
import pytest
from faker import Faker

from src.api.controllers.test_controller import TestController
from src.api.models import Project, Test

fake = Faker()


def assert_valid_test(test: Test, expected_title: str | None = None) -> None:
    assert isinstance(test, Test)
    assert test.id is not None
    assert test.type == "test"
    assert test.attributes is not None
    if expected_title:
        assert test.attributes.title == expected_title


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


@pytest.mark.api
def test_delete_test_removes_it(
    test_controller: TestController,
    project: Project,
    new_test: Test,
):
    test_controller.delete(project_id=project.id, test_id=new_test.id)

    with pytest.raises(httpx.HTTPStatusError) as exc_info:
        test_controller.get_by_id(project_id=project.id, test_id=new_test.id)

    assert exc_info.value.response.status_code == 404


@pytest.mark.api
def test_create_test_with_invalid_suite_id_returns_404(
    test_controller: TestController,
    project: Project,
):
    with pytest.raises(httpx.HTTPStatusError) as exc_info:
        test_controller.create(
            project_id=project.id,
            suite_id="non-existent-suite",
            title=fake.sentence(),
        )

    assert exc_info.value.response.status_code == 404
