from playwright.sync_api import Page

from src.web.components.ProjectCard import ProjectCard
from src.web.components.ProjectPageHeader import ProjectPageHeader


class ProjectsPage:
    def __init__(self, page: Page):
        self.page = page
        self.header = ProjectPageHeader(page)

    def is_loaded(self):
        self.header.is_loaded()

    def get_project_card(self, project_name: str) -> ProjectCard:
        return ProjectCard(self.page, project_name)
