import pytest

from src.web.application import Application
from tests.fixtures.cookie_helper import CookieHelper


@pytest.mark.smoke
@pytest.mark.web
def test_add_feature_flag_cookie(logged_app: Application, logged_cookies: CookieHelper):
    logged_cookies.add(name="feature_flag", value="dark_mode_enabled", domain="app.testomat.io")

    assert logged_cookies.exists("feature_flag")
    assert logged_cookies.get_value("feature_flag") == "dark_mode_enabled"
    logged_app.page.reload()


@pytest.mark.web
def test_clear_feature_flag_cookie(logged_app: Application, logged_cookies: CookieHelper):
    logged_cookies.add(name="feature_flag", value="beta_feature", domain="app.testomat.io")
    assert logged_cookies.exists("feature_flag")

    logged_cookies.clear(name="feature_flag")
    assert not logged_cookies.exists("feature_flag")
