import pytest
from faker import Faker

from src.web.Application import Application
from tests.conftest import Config

fake = Faker()

invalid_credentials = [
    pytest.param(fake.email(), fake.password(length=10), id="ecp_unregistered_email"),
    pytest.param(fake.user_name(), fake.password(length=10), id="ecp_email_missing_at"),
    pytest.param("invalid@", fake.password(length=10), id="ecp_email_missing_domain"),
    pytest.param("adomain.com", fake.password(length=10), id="ecp_email_missing_local_part"),
    pytest.param("user@@domain.com", fake.password(length=10), id="ecp_email_double_at"),
    pytest.param("user named@domain.com", fake.password(length=10), id="ecp_email_with_space"),
    pytest.param(None, fake.password(length=10), id="ecp_wrong_password"),
    pytest.param(None, " ", id="ecp_password_only_spaces"),
    pytest.param("", "", id="bva_both_empty"),
    pytest.param("", fake.password(length=10), id="bva_empty_email"),
    pytest.param(None, "", id="bva_password_length_0"),
    pytest.param(None, fake.password(length=1, special_chars=False, upper_case=False, lower_case=False),
                 id="bva_password_length_1"),
    pytest.param("a@b.c", fake.password(length=10), id="bva_min_valid_email"),
    pytest.param(f"{'a' * 64}@{'b' * 63}.com", fake.password(length=10), id="bva_max_length_email"),
    pytest.param(None, fake.password(length=72), id="bva_password_bcrypt_boundary"),
    pytest.param(None, fake.password(length=73), id="bva_password_bcrypt_boundary_plus1"),
]


@pytest.mark.parametrize("email, password", invalid_credentials)
def test_login_invalid(shared_app: Application, configs: Config, email, password: str):
    actual_email = configs.email if email is None else email

    shared_app.login_page.open()
    shared_app.login_page.is_loaded()
    shared_app.login_page.login_user(actual_email, password)
    shared_app.login_page.invalid_login_message_visible()


def test_login_with_valid_creds(app: Application, configs: Config):
    app.home_page.open()
    app.home_page.is_loaded()
    app.home_page.click_login()

    app.login_page.is_loaded()
    app.login_page.login_user(configs.email, configs.password)
    app.projects_page.is_loaded()
