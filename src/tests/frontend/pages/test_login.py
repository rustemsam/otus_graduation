import allure
import pytest

from src.main.frontend.helper.config_helper import ConfigHelper
from src.main.frontend.model.login_model import LoginModel
from src.main.frontend.pages.alert_element import AlertErrorElement
from src.main.frontend.pages.login_page import LoginPage
from src.main.frontend.pages.orm.dashboard_page import DashboardPage
from src.main.frontend.pages.password_reset_page import PasswordResetPage


@allure.title("Check the login to the admin panel")
def test_login(browser):
    login_page = LoginPage(browser)
    login_page.login_to_admin_panel(
        ConfigHelper.get_key("ADMIN_LOGIN"), ConfigHelper.get_key("ADMIN_PASSWORD")
    )
    dashboard_page = DashboardPage(browser)
    dashboard_list = dashboard_page.get_list_available_dashboards()

    expected_list = [
        "Time at Work",
        "My Actions",
        "Quick Launch",
        "Employees on Leave Today",
        "Employee Distribution by Sub Unit",
        "Employee Distribution by Location",
    ]
    assert set(expected_list).issubset(set(dashboard_list)), (
        f"Expected list elements {expected_list} to be present in {dashboard_list}, but some are missing."
    )


@allure.title("Check the validation message when trying to login with wrong password")
def test_login_with_wrong_password(browser):
    login_page = LoginPage(browser)

    login_page.login_to_admin_panel(ConfigHelper.get_key("ADMIN_LOGIN"), "qwerty123")

    alert = AlertErrorElement(browser)
    text = alert.get_failure_text_alert()
    expected_text = "Invalid credentials"
    assert text == expected_text, f"Expected text is {expected_text}, but got {text}"


@allure.title(
    "Check the validation message when trying to login without mandatory fields"
)
@pytest.mark.parametrize(
    "post_request",
    [
        LoginModel(
            username="test",
        ),
        LoginModel(password="test"),
    ],
)
def test_login_without_mandatory_fields(browser, post_request):
    login_page = LoginPage(browser)

    if post_request.username is not None:
        login_page.fill_username(post_request.username)
    if post_request.password is not None:
        login_page.fill_password(post_request.password)

    login_page.click_for_login()
    alert = AlertErrorElement(browser)
    text = alert.get_input_field_text_alert()

    expected_alert_text = "Required"
    assert text == expected_alert_text, (
        f"Expected '{expected_alert_text}', but got '{text}'"
    )


@allure.title("Check the option of resetting password")
def test_reset_password(browser):
    login_page = LoginPage(browser)

    login_page.forgot_password()

    password_reset_page = PasswordResetPage(browser)
    password_reset_page.reset_password("test")
    text = password_reset_page.get_reset_password_confirmation()
    expected_text = "Reset Password link sent successfully"
    assert text == expected_text, f"Expected text is {expected_text}, but got {text}"


@allure.title("Check cancel of resetting password")
def test_cancel_reset_password(browser):
    login_page = LoginPage(browser)

    login_page.forgot_password()

    password_reset_page = PasswordResetPage(browser)
    password_reset_page.click_cancel()
    login_page = LoginPage(browser)
    text = login_page.get_login_title_text()
    expected_text = "Login"
    assert text == expected_text, f"Expected text is {expected_text}, but got {text}"
