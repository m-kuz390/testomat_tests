from typing import Self

from playwright.sync_api import Page, expect


class HomePage:
    def __init__(self, page: Page) -> None:
        self.page = page

    def open(self) -> Self:
        self.page.goto("https://testomat.io")
        return self

    def is_loaded(self) -> Self:
        expect(self.page.locator("#headerMenuWrapper")).to_be_visible()
        expect(self.page.locator(".side-menu .login-item")).to_have_text("Log in")
        expect(self.page.locator(".side-menu .start-item")).to_have_text("Start for free")
        return self

    def click_login(self) -> Self:
        self.page.get_by_text("Log in", exact=True).click()
        return self

    def click_start_free_trial(self) -> Self:
        self.page.locator(".side-menu .start-item").click()
        return self
