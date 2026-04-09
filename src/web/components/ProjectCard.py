from playwright.sync_api import Page, expect


class ProjectCard:
    def __init__(self, page: Page, project_name: str):
        self.page = page
        self.project_name = project_name
        self._card = page.locator("li").filter(has=page.get_by_role("heading", name=project_name, exact=True))

    def is_visible(self):
        expect(self._card).to_be_visible()

    def is_hidden(self):
        expect(self._card).to_be_hidden()

    def get_title(self) -> str:
        return self._card.locator("h3").inner_text()

    def get_tests_count(self) -> str:
        return self._card.locator("p.text-gray-500").inner_text()

    def get_badge(self):
        return self._card.locator(".common-badge")

    def click(self):
        self._card.locator("a").click()
