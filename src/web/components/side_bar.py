import allure
import re
from typing import Self

from playwright.sync_api import Page, expect


class SideBar:
    def __init__(self, page: Page) -> None:
        self.page = page
        self._sidebar = page.locator(".mainnav-menu")

    @allure.step
    def is_loaded(self) -> Self:
        expect(self._sidebar).to_be_visible()
        return self

    @allure.step
    def click_logo(self) -> Self:
        self._sidebar.locator("span.btn-open").click(force=True)
        return self

    @allure.step
    def close(self) -> Self:
        self._sidebar.get_by_role("button").click()
        return self

    @allure.step
    def navigate_to(self, section: str) -> Self:
        self._sidebar.get_by_role("link", name=section).click()
        return self

    @allure.step
    def go_to_tests(self) -> Self:
        return self.navigate_to("Tests")

    @allure.step
    def go_to_requirements(self) -> Self:
        return self.navigate_to("Requirements")

    @allure.step
    def go_to_runs(self) -> Self:
        return self.navigate_to("Runs")

    @allure.step
    def go_to_plans(self) -> Self:
        return self.navigate_to("Plans")

    @allure.step
    def go_to_steps(self) -> Self:
        return self.navigate_to("Steps")

    @allure.step
    def go_to_pulse(self) -> Self:
        return self.navigate_to("Pulse")

    @allure.step
    def go_to_imports(self) -> Self:
        return self.navigate_to("Imports")

    @allure.step
    def go_to_analytics(self) -> Self:
        return self.navigate_to("Analytics")

    @allure.step
    def go_to_branches(self) -> Self:
        return self.navigate_to("Branches")

    @allure.step
    def go_to_settings(self) -> Self:
        return self.navigate_to("Settings")

    @allure.step
    def go_to_help(self) -> Self:
        return self.navigate_to("Help")

    @allure.step
    def go_to_projects(self) -> Self:
        return self.navigate_to("Projects")

    @allure.step
    def is_section_active(self, section: str) -> Self:
        expect(self._sidebar.get_by_role("link", name=section)).to_have_class(re.compile(r"\bactive\b"))
        return self

    @allure.step
    def is_tab_active(self, section: str) -> bool:
        link = self._sidebar.get_by_role("link", name=section)
        classes = link.get_attribute("class") or ""
        return bool(re.search(r"\bactive\b", classes))

    @allure.step
    def get_username(self) -> str:
        return self._sidebar.locator(".label-container").last.inner_text().strip()
