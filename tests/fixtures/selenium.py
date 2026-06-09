import os

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

IS_CI = bool(os.getenv("CI"))


@pytest.fixture(scope="function")
def driver():
    options = Options()
    if IS_CI:
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(0)
    driver.maximize_window()
    yield driver
    driver.quit()
