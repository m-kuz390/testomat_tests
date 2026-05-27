import pytest
from selenium import webdriver


@pytest.fixture(scope="function")
def driver():
    driver = webdriver.Chrome()
    driver.implicitly_wait(0)
    driver.maximize_window()
    yield driver
    driver.quit()
