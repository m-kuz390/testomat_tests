from playwright.sync_api import Page, expect


def login_with_invalid_creds(page: Page):
    page.goto('https://testomat.io')

    expect(page.locator("[href*='sign_in'].login-item")).to_be_visible()

    page.get_by_text("Log in", exact=True).click()

    # page.get_by_role("textbox", name="name@email.com")
    page.locator("#content-desktop #user_email").fill("m.kuz390@gmail.com")
    page.locator("#content-desktop #user_password").fill("Zaqq1234567890!")
    page.get_by_role("button", name="Sign In").click()

    expect(page.locator("#content-desktop").get_by_text("Invalid Email or password")).to_be_visible()

    # expect(page).to_have_title("AI Test Management Tool | Testomat.io")

