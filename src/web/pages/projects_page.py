from typing import Self

from playwright.sync_api import Page

from src.web.components.project_card import ProjectCard
from src.web.components.project_page_header import ProjectPageHeader


class ProjectsPage:
    def __init__(self, page: Page) -> None:
        self.page = page
        self.header = ProjectPageHeader(page)

    def is_loaded(self) -> Self:
        self.header.is_loaded()
        return self

    def get_project_card(self, project_name: str) -> ProjectCard:
        return ProjectCard(self.page, project_name)
