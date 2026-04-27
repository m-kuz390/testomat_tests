from typing import Self

from playwright.sync_api import Locator, Page, expect


class ProjectPageHeader:
    def __init__(self, page: Page) -> None:
        self.page = page

    def is_loaded(self) -> Self:
        expect(self.page.locator(".common-page-header")).to_be_visible()
        expect(self.page.locator(".common-page-header h2")).to_have_text("Projects")
        return self

    def get_selected_company(self) -> Locator:
        return self.page.locator("#company_id")

    def get_plan_name(self) -> Locator:
        return self.page.locator(".tooltip-project-plan span").last

    def select_company(self, company_name: str) -> Self:
        self.page.locator("#company_id").select_option(label=company_name)
        return self

    def search_project(self, project_name: str) -> Self:
        self.page.locator("#content-desktop #search").fill(project_name)
        return self

    def click_create(self) -> Self:
        self.page.locator(".common-page-header-right").get_by_role("link", name="Create").click()
        return self

    def switch_to_grid_view(self) -> Self:
        self.page.locator("#grid-view").click()
        return self

    def switch_to_table_view(self) -> Self:
        self.page.locator("#table-view").click()
        return self

    def is_grid_view_active(self) -> Self:
        expect(self.page.locator("#grid-view")).to_have_class("tablinks active_list_type")
        return self

    def is_table_view_active(self) -> Self:
        expect(self.page.locator("#table-view")).to_have_class("tablinks active_list_type")
        return self
