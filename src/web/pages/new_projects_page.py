from typing import Self

from playwright.sync_api import Page, expect

from src.web.pages.project_page import ProjectPage


class NewProjectsPage:
    def __init__(self, page: Page) -> None:
        self.page = page
        self._form_container = page.locator("#content-desktop [action='/projects']")

    def open(self) -> Self:
        self.page.goto("/projects/new")
        return self

    def is_loaded(self) -> Self:
        expect(self._form_container).to_be_visible()
        expect(self._form_container.locator("#classical")).to_be_visible()
        expect(self._form_container.locator("#classical")).to_contain_text("Classical")
        expect(self._form_container.locator("#bdd")).to_be_visible()
        expect(self._form_container.locator("#bdd")).to_contain_text("BDD")
        expect(self._form_container.locator("#project_title")).to_be_visible()
        expect(self._form_container.locator("#demo-btn")).to_be_visible()
        expect(self._form_container.locator("#project-create-btn")).to_be_visible()
        expect(self.page.get_by_text("How to start?")).to_be_visible()
        expect(self.page.get_by_text("New Project")).to_be_visible()
        return self

    def fill_project_till(self, target_project_name: str) -> Self:
        self._form_container.locator("#project_title").fill(target_project_name)
        return self

    def click_create(self) -> ProjectPage:
        self._form_container.locator("#project-create-btn input").click()
        expect(self._form_container.locator("#project-create-btn input")).to_be_hidden(timeout=10_000)
        return ProjectPage(self.page)
