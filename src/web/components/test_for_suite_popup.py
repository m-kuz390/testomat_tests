from __future__ import annotations

from playwright.sync_api import Page, expect


class TestForSuitePopup:
    def __init__(self, page: Page):
        self.page = page
        self.suite_items = page.locator("li[role='button']")

    def is_loaded(self) -> TestForSuitePopup:
        expect(self.page.get_by_role("heading", name="Select suite for test")).to_be_visible()
        expect(self.suite_items.first).to_be_visible()
        return self

    def select_first_suite(self) -> TestForSuitePopup:
        self.suite_items.first.click()
        self.page.get_by_role("button", name="Select").click()
        return self
