import allure
import pytest
from faker import Faker

from src.main.frontend.helper.config_helper import ConfigHelper
from src.main.frontend.model.pim_employee_model import PimEmployeeModel
from src.main.frontend.pages.alert_element import AlertErrorElement
from src.main.frontend.pages.login_page import LoginPage
from src.main.frontend.pages.orm.pim_page import PimPage

fake = Faker()


@pytest.fixture
def login_as_admin(browser):
    """Log in to the admin panel and return an instance of PimPage."""
    login_page = LoginPage(browser)
    login_page.login_to_admin_panel(
        ConfigHelper.get_key("ADMIN_LOGIN"), ConfigHelper.get_key("ADMIN_PASSWORD")
    )
    return PimPage(browser)


@allure.title("Check count of records based on employment status")
@pytest.mark.parametrize(
    "employment_status",
    ["Freelance", "Part-Time Contract"],
)
def test_count_of_records(browser, login_as_admin, employment_status):
    pim_page = login_as_admin
    pim_page.select_employment_status(employment_status)
    pim_page.click_search()
    rows = pim_page.get_list_available_pim_records()
    assert len(rows) == 0, f"Expected 0 matching rows, but found {len(rows)}"


@allure.title("Add employee to pim without creating login details")
def test_add_employee_without_creating_login_details(browser, login_as_admin):
    pim_page = login_as_admin
    pim_page.click_add_button()
    pim_page.fill_personal_details(first=fake.first_name())
    pim_page.fill_personal_details(last=fake.last_name())
    pim_page.personal_info.click_save()

    actual_text = pim_page.get_pim_title()
    expected_text = "Personal Details"
    assert actual_text == expected_text, (
        f"Expected text is '{expected_text}', but got '{actual_text}'"
    )


@allure.title("Add employee to pim with creating login details")
def test_add_employee_with_creating_login_details(browser, login_as_admin):
    pim_page = login_as_admin
    pim_page.click_add_button()
    pim_page.fill_personal_details(first=fake.first_name())
    pim_page.fill_personal_details(last=fake.last_name())
    pim_page.click_create_login_details_button()
    password = fake.password()
    pim_page.fill_login_details(fake.user_name(), password, password)
    pim_page.personal_info.click_save()

    actual_text = pim_page.get_pim_title()
    expected_text = "Personal Details"
    assert actual_text == expected_text, (
        f"Expected text is '{expected_text}', but got '{actual_text}'"
    )


@allure.title(
    "Check validation message for invalid login details when creating an employee"
)
@pytest.mark.parametrize(
    "login_data, error_message",
    [
        (
            PimEmployeeModel(
                username=fake.user_name(),
                password=fake.password(length=8),
                confirm_password=fake.password(length=9),
            ),
            "Passwords do not match",
        ),
        (
            PimEmployeeModel(
                username="abc", password="qwerty123", confirm_password="qwerty123"
            ),
            "Should be at least 5 characters",
        ),
        (
            PimEmployeeModel(
                username=fake.user_name(), password="qwerty", confirm_password="qwerty"
            ),
            "Should have at least 7 characters",
        ),
    ],
)
def test_add_employee_with_invalid_login_details(
    browser, login_as_admin, login_data, error_message
):
    pim_page = login_as_admin
    pim_page.click_add_button()

    pim_page.fill_personal_details(first=fake.first_name(), last=fake.last_name())

    pim_page.click_create_login_details_button()
    pim_page.fill_login_details(
        login_data.username, login_data.password, login_data.confirm_password
    )

    pim_page.personal_info.click_save()
    alert = AlertErrorElement(browser)
    actual_text = alert.get_input_field_text_alert()

    assert actual_text == error_message, (
        f"Expected text is '{error_message}', but got '{actual_text}'"
    )