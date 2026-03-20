from playwright.sync_api import Page, expect


def open_home_page(page: Page):
    page.goto("https://testomat.io")


def open_login_form(page: Page):
    page.get_by_text("Log in", exact=True).click()


def fill_login_form(page: Page, email: str, password: str):
    page.locator("#content-desktop #user_email").fill(email)
    page.locator("#content-desktop #user_password").fill(password)


def submit_login(page: Page):
    page.get_by_role("button", name="Sign In").click()


def click_start_free_trial(page: Page):
    page.locator(".side-menu .start-item").click()


def test_login_with_invalid_creds(page: Page):
    open_home_page(page)
    expect(page.locator("[href*='sign_in'].login-item")).to_be_visible()


    open_login_form(page)
    fill_login_form(page, "m.kuz390@gmail.com", "Zaqq1234567890!")
    submit_login(page)

    expect(page.locator("#content-desktop").get_by_text("Invalid Email or password")).to_be_visible()
    expect(page.locator("#content-desktop .common-flash-info")).to_have_text("Invalid Email or password.")


def test_login_success(page: Page):
    open_home_page(page)
    open_login_form(page)
    fill_login_form(page, "m.kuz390@gmail.com", "Zaqq123456789!")
    submit_login(page)

    expect(page).to_have_url("https://app.testomat.io/")
    expect(page.locator(".common-flash-success").get_by_text("Signed in successfully")).to_be_visible()


def test_start_free_trial(page: Page):
    open_home_page(page)

    expect(page.locator(".side-menu .start-item")).to_be_visible()

    click_start_free_trial(page)

    expect(page).to_have_url("https://app.testomat.io/users/sign_up")


def test_open_project(page: Page):
    open_home_page(page)
    open_login_form(page)
    fill_login_form(page, "m.kuz390@gmail.com", "Zaqq123456789!")
    submit_login(page)

    expect(page.locator("#company_id")).to_contain_text("QA Club Lviv")

    expect(page.get_by_role("link", name="Grocery, Outdoors & Shoes")).to_be_visible()
    page.get_by_role("link", name="Grocery, Outdoors & Shoes").click()

    expect(page).to_have_url("https://app.testomat.io/projects/grocery-outdoors-shoes/")


def test_open_create_project(page: Page):
    open_home_page(page)
    open_login_form(page)
    fill_login_form(page, "m.kuz390@gmail.com", "Zaqq123456789!")
    submit_login(page)

    page.locator("#company_id").select_option(label="Free Projects")

    expect(page.get_by_text("You have not created any projects yet")).to_be_visible()

    page.get_by_role("link", name="Create project").click()

    expect(page).to_have_url("https://app.testomat.io/projects/new")