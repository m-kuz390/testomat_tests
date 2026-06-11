import pytest
from selenium.common import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from tests.fixtures.config import Config
from web.selenium.pages.login_page import LoginPage
from web.selenium.pages.login_page_v2 import LoginPageV2


@pytest.mark.regression
@pytest.mark.web
@pytest.mark.selenium
def test_selenium_login_and_search(driver: WebDriver, configs: Config):
    wait = WebDriverWait(
        driver=driver,
        timeout=10,
        poll_frequency=0.1,
        ignored_exceptions=[NoSuchElementException, StaleElementReferenceException],
    )

    driver.get(configs.login_url)
    driver.find_element(by=By.CSS_SELECTOR, value="#content-desktop #user_email").send_keys(configs.email)
    driver.find_element(by=By.CSS_SELECTOR, value="#content-desktop #user_password").send_keys(configs.password)
    driver.find_element(by=By.CSS_SELECTOR, value="#content-desktop [value='Sign In']").click()
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#content-desktop .common-flash-success")))

    target_project = "test123"
    driver.find_element(by=By.CSS_SELECTOR, value="#content-desktop #search").send_keys(target_project)
    driver.find_element(by=By.CSS_SELECTOR, value=f"#content-desktop [title='{target_project}']").click()
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, f".breadcrumbs-page [title='{target_project}']")))


@pytest.mark.smoke
@pytest.mark.web
@pytest.mark.selenium
def test_login_with_page_object_v1(driver: WebDriver, configs: Config):
    login_page = LoginPage(driver)
    login_page.open(configs.login_url)
    login_page.is_loaded()
    login_page.login(email=configs.email, password=configs.password)
    login_page.should_see_success_message()


@pytest.mark.regression
@pytest.mark.web
@pytest.mark.selenium
def test_login_with_page_object_v2(driver: WebDriver, configs: Config):
    login_page = LoginPageV2(driver)
    login_page.open(configs.login_url)
    login_page.is_loaded()
    login_page.login(email=configs.email, password=configs.password)
    login_page.should_see_success_message()


@pytest.mark.regression
@pytest.mark.web
@pytest.mark.selenium
def test_login_page_url(driver: WebDriver, configs: Config):
    wait = WebDriverWait(driver=driver, timeout=10)
    driver.get(configs.login_url)
    wait.until(EC.url_contains("sign_in"))


@pytest.mark.regression
@pytest.mark.web
@pytest.mark.selenium
def test_login_with_remember_me(driver: WebDriver, configs: Config):
    login_page = LoginPage(driver)
    login_page.open(configs.login_url)
    login_page.is_loaded()
    login_page.login(email=configs.email, password=configs.password, remember_me=True)
    login_page.should_see_success_message()


@pytest.mark.regression
@pytest.mark.web
@pytest.mark.selenium
def test_switch_projects_view(driver: WebDriver, configs: Config):
    wait = WebDriverWait(
        driver=driver,
        timeout=10,
        poll_frequency=0.1,
        ignored_exceptions=[NoSuchElementException, StaleElementReferenceException],
    )

    driver.get(configs.login_url)
    driver.find_element(by=By.CSS_SELECTOR, value="#content-desktop #user_email").send_keys(configs.email)
    driver.find_element(by=By.CSS_SELECTOR, value="#content-desktop #user_password").send_keys(configs.password)
    driver.find_element(by=By.CSS_SELECTOR, value="#content-desktop [value='Sign In']").click()
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#content-desktop .common-flash-success")))

    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#table-view"))).click()
    wait.until(lambda d: "active_list_type" in d.find_element(By.CSS_SELECTOR, "#table-view").get_attribute("class"))

    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#grid-view"))).click()
    wait.until(lambda d: "active_list_type" in d.find_element(By.CSS_SELECTOR, "#grid-view").get_attribute("class"))
