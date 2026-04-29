import pytest

from src.web.application import Application
from tests.fixtures.cookie_helper import CookieHelper


@pytest.mark.smoke
@pytest.mark.web
def test_add_feature_flag_cookie(logged_app: Application, cookies: CookieHelper):
    """Verify that a feature flag cookie can be added and retrieved."""
    cookies.add(name="feature_flag", value="dark_mode_enabled", domain="app.testomat.io")

    assert cookies.exists("feature_flag")
    assert cookies.get_value("feature_flag") == "dark_mode_enabled"
    logged_app.page.reload()
    # do some staff


@pytest.mark.web
def test_clear_feature_flag_cookie(logged_app: Application, cookies: CookieHelper):
    """Verify that a feature flag cookie can be cleared."""
    cookies.add(name="feature_flag", value="beta_feature", domain="app.testomat.io")
    assert cookies.exists("feature_flag")

    cookies.clear(name="feature_flag")
    assert not cookies.exists("feature_flag")
