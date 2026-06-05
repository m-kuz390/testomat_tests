from src.api.controllers.base_controller import BaseController
from src.api.models import Test


class TestController(BaseController):
    def create(self, project_id: str, suite_id: str, title: str, description: str | None = None) -> Test:
        payload = {
            "data": {
                "type": "tests",
                "attributes": {"title": title, "description": description},
                "relationships": {
                    "suite": {"data": {"type": "suites", "id": suite_id}}
                },
            }
        }
        data = self._post(f"/api/{project_id}/tests", payload)
        return Test.model_validate(data["data"])

    def get_by_id(self, project_id: str, test_id: str) -> Test:
        data = self._get(f"/api/{project_id}/tests/{test_id}")
        return Test.model_validate(data["data"])

    def delete(self, project_id: str, test_id: str) -> None:
        self._delete(f"/api/{project_id}/tests/{test_id}")
