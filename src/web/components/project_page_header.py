from typing import Self

import allure
from playwright.sync_api import Locator, Page, expect


class ProjectPageHeader:
    def __init__(self, page: Page) -> None:
        self.page = page
        self.enterprise_plan_label = page.get_by_text("Enterprise plan")
        self.free_plan_label = page.get_by_text("Free plan")

    @allure.step
    def is_loaded(self) -> Self:
        expect(self.page.locator(".common-page-header")).to_be_visible()
        expect(self.page.locator(".common-page-header h2")).to_have_text("Projects")
        return self

    @allure.step
    def get_selected_company(self) -> Locator:
        return self.page.locator("#company_id")

    @allure.step
    def get_plan_name(self) -> Locator:
        return self.page.locator(".tooltip-project-plan span").last

    @allure.step
    def select_company(self, company_name: str) -> Self:
        self.page.locator("#company_id").select_option(label=company_name)
        self.page.goto(self.page.url)
        return self

    @allure.step
    def search_project(self, project_name: str) -> Self:
        self.page.wait_for_function("typeof run_search_project !== 'undefined'")
        self.page.locator("#content-desktop #search").type(project_name)
        return self

    @allure.step
    def click_create(self) -> Self:
        self.page.locator(".common-page-header-right").get_by_role("link", name="Create").click()
        return self

    @allure.step
    def switch_to_grid_view(self) -> Self:
        self.page.locator("#grid-view").click()
        return self

    @allure.step
    def switch_to_table_view(self) -> Self:
        self.page.locator("#table-view").click()
        return self

    @allure.step
    def is_grid_view_active(self) -> Self:
        expect(self.page.locator("#grid-view")).to_have_class("tablinks active_list_type")
        return self

    @allure.step
    def is_table_view_active(self) -> Self:
        expect(self.page.locator("#table-view")).to_have_class("tablinks active_list_type")
        return self
