import os

import pytest
from faker import Faker
from playwright.sync_api import Page, expect

from tests.conftest import Config

TARGET_PROJECT = "Grocery, Outdoors & Shoes"


@pytest.fixture(scope="function")
def login(page: Page, configs: Config):
    page.goto(configs.login_url)
    login_user(page, configs.email, configs.password)


def test_login_with_invalid_creds(page: Page, configs):
    open_home_page(page)
    expect(page.locator("[href*='sign_in'].login-item")).to_be_visible()

    invalid_password = Faker().password(length=10)

    open_login_form(page)
    login_user(page, configs.email, invalid_password)

    expect(page.locator("#content-desktop").get_by_text("Invalid email or password")).to_be_visible()
    expect(page.locator("#content-desktop .common-flash-info")).to_have_text("Invalid email or password.")


def test_login_success(page: Page, configs: Config):
    open_home_page(page)
    open_login_form(page)
    login_user(page, configs.email, configs.password)

    expect(page).to_have_url("https://app.testomat.io/")
    expect(page.locator(".common-flash-success").get_by_text("Signed in successfully")).to_be_visible()


def test_start_free_trial(page: Page):
    open_home_page(page)

    expect(page.locator(".side-menu .start-item")).to_be_visible()

    click_start_free_trial(page)

    expect(page).to_have_url("https://app.testomat.io/users/sign_up")


def test_open_project(page: Page, configs: Config):
    open_home_page(page)
    open_login_form(page)
    login_user(page, configs.email, configs.password)

    expect(page.locator("#company_id")).to_contain_text("QA Club Lviv")

    expect(page.get_by_role("link", name="Grocery, Outdoors & Shoes")).to_be_visible()
    page.get_by_role("link", name="Grocery, Outdoors & Shoes").click()

    expect(page).to_have_url("https://app.testomat.io/projects/grocery-outdoors-shoes/")


def test_open_create_project(page: Page, configs: Config):
    open_home_page(page)
    open_login_form(page)
    login_user(page, configs.email, configs.password)

    page.locator("#company_id").select_option(label="Free Projects")

    expect(page.get_by_text("You have not created any projects yet")).to_be_visible()

    page.get_by_role("link", name="Create project").click()

    expect(page).to_have_url("https://app.testomat.io/projects/new")


def test_search_project_in_company(page: Page, login):
    search_for_project(page, TARGET_PROJECT)

    expect(page.get_by_role("heading", name=TARGET_PROJECT)).to_be_visible()


def test_should_be_possible_to_open_free_project(page: Page, login):
    page.locator("#company_id").click()
    page.locator("#company_id").select_option("Free Projects")

    search_for_project(page, TARGET_PROJECT)
    expect(page.get_by_role("heading", name=TARGET_PROJECT)).to_be_hidden()

    expect(page.get_by_text("You have not created any projects yet")).to_be_visible(timeout=10000)


def open_home_page(page: Page):
    page.goto(os.getenv("BASE_URL"))


def open_login_form(page: Page):
    page.get_by_text("Log in", exact=True).click()


def login_user(page: Page, email: str, password: str):
    page.locator("#content-desktop #user_email").fill(email)
    page.locator("#content-desktop #user_password").fill(password)
    page.get_by_role("button", name="Sign In").click()


def click_start_free_trial(page: Page):
    page.locator(".side-menu .start-item").click()


def search_for_project(page: Page, target_project: str):
    expect(page.get_by_role("searchbox", name="Search")).to_be_visible()
    page.locator("#content-desktop #search").fill(target_project)
