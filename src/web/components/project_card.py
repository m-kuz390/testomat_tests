from typing import Self

from playwright.sync_api import Locator, Page, expect


class ProjectCard:
    def __init__(self, page: Page, project_name: str) -> None:
        self.page = page
        self.project_name = project_name
        self._card = page.locator("li").filter(has=page.get_by_role("heading", name=project_name, exact=True))

    def is_visible(self) -> Self:
        expect(self._card).to_be_visible()
        return self

    def is_hidden(self) -> Self:
        expect(self._card).to_be_hidden()
        return self

    def get_title(self) -> str:
        return self._card.locator("h3").inner_text()

    def get_tests_count(self) -> str:
        return self._card.locator("p.text-gray-500").inner_text()

    def get_badge(self) -> Locator:
        return self._card.locator(".common-badge")

    def click(self) -> Self:
        self._card.locator("a").click()
        return self
