from src.api.controllers.base_controller import BaseController
from src.api.models import Project


class ProjectController(BaseController):
    def get_all(self) -> list[Project]:
        data = self._get("/api/projects")
        return [Project.model_validate(p) for p in data["data"]]

    def get_by_id(self, project_id: str) -> Project:
        data = self._get(f"/api/projects/{project_id}")
        return Project.model_validate(data["data"])
