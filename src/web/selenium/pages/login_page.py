import allure
from typing import Self

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from src.web.selenium.core.base_page import BasePage


class LoginPage(BasePage):
    EMAIL_INPUT = (By.CSS_SELECTOR, "#content-desktop #user_email")
    PASSWORD_INPUT = (By.CSS_SELECTOR, "#content-desktop #user_password")
    REMEMBER_ME_CHECKBOX = (By.CSS_SELECTOR, "#user_remember_me")
    SIGN_IN_BUTTON = (By.CSS_SELECTOR, "#content-desktop [value='Sign In']")
    SUCCESS_MESSAGE = (By.CSS_SELECTOR, "#content-desktop .common-flash-success")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "#content-desktop .common-flash-info")
    INVALID_LOGIN_TEXT = (By.XPATH, "//*[contains(text(), 'Invalid Email or password')]")

    def __init__(self, driver: WebDriver):
        super().__init__(driver)

    @allure.step
    def open(self, base_url: str = "") -> Self:
        self.driver.get(f"{base_url}/users/sign_in")
        return self

    @allure.step
    def is_loaded(self) -> Self:
        self.wait.for_visible(self.EMAIL_INPUT)
        self.wait.for_visible(self.PASSWORD_INPUT)
        return self

    @allure.step
    def check_remember_me(self) -> Self:
        checkbox = self.find(self.REMEMBER_ME_CHECKBOX)
        if not checkbox.is_selected():
            self.driver.execute_script("arguments[0].click();", checkbox)
        return self

    @allure.step
    def login(self, email: str, password: str, remember_me: bool = False) -> Self:
        self.type_text(target=self.EMAIL_INPUT, text=email)
        self.type_text(target=self.PASSWORD_INPUT, text=password)

        if remember_me:
            self.check_remember_me()

        self.click(self.SIGN_IN_BUTTON)
        return self

    @allure.step
    def should_see_success_message(self) -> Self:
        self.wait.for_visible(self.SUCCESS_MESSAGE)
        return self

    @allure.step
    def should_see_invalid_login_error(self) -> Self:
        self.wait.for_visible(self.ERROR_MESSAGE)
        return self
