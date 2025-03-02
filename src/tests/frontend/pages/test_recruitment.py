import allure
import pytest
from faker import Faker

from src.main.frontend.helper.config_helper import ConfigHelper
from src.main.frontend.model.candidate_model import CandidateModel
from src.main.frontend.pages.alert_element import AlertErrorElement
from src.main.frontend.pages.login_page import LoginPage
from src.main.frontend.pages.orm.recruitment_page import RecruitmentPage

fake = Faker()


@pytest.fixture
def login_as_admin(browser):
    """Log in to the admin panel and return an instance of RecruitmentPage."""
    login_page = LoginPage(browser)
    login_page.login_to_admin_panel(
        ConfigHelper.get_key("ADMIN_LOGIN"), ConfigHelper.get_key("ADMIN_PASSWORD")
    )
    return RecruitmentPage(browser)


def fill_candidate_details(recruitment_page, candidate_data: CandidateModel = None):
    """
    Fill candidate details using the provided candidate_data or Faker data if not provided.
    """
    if candidate_data:
        if candidate_data.first_name:
            recruitment_page.fill_personal_details(first=candidate_data.first_name)
        else:
            recruitment_page.fill_personal_details(first=fake.first_name())
        if candidate_data.last_name:
            recruitment_page.fill_personal_details(first=candidate_data.last_name)
        else:
            recruitment_page.fill_personal_details(last=fake.last_name())
        if candidate_data.email:
            recruitment_page.fill_personal_details(email=candidate_data.email)
        else:
            recruitment_page.fill_personal_details(email=fake.email())
    else:
        recruitment_page.fill_personal_details(first=fake.first_name())
        recruitment_page.fill_personal_details(middle=fake.name())
        recruitment_page.fill_personal_details(last=fake.last_name())
        recruitment_page.fill_personal_details(email=fake.email())
        recruitment_page.fill_application_date(fake.date())


@allure.title("Check option of adding candidate")
def test_add_candidate_success(browser, login_as_admin):
    recruitment_page = login_as_admin
    recruitment_page.click_add_candidate()
    role_name = "Junior Account Assistant"
    recruitment_page.select_candidate(role_name)
    fill_candidate_details(recruitment_page)
    recruitment_page.click_consent_checkbox()
    recruitment_page.personal_info.click_save()

    actual_text = recruitment_page.get_application_stage_title()
    expected_text = "Application Stage"
    assert actual_text == expected_text, (
        f"Expected text is '{expected_text}', but got '{actual_text}'"
    )


@allure.title(
    "Check the validation message when creating a candidate without mandatory fields"
)
@pytest.mark.parametrize(
    "candidate_data",
    [
        CandidateModel(first_name="test", email="email@email.com"),
        CandidateModel(first_name="test", last_name="test"),
        CandidateModel(last_name="test", email="email@email.com"),
    ],
)
def test_candidate_creation_without_mandatory_fields(
    browser, candidate_data, login_as_admin
):
    recruitment_page = login_as_admin
    recruitment_page.click_add_candidate()

    if candidate_data.first_name:
        recruitment_page.fill_personal_details(first=candidate_data.first_name)
    if candidate_data.last_name:
        recruitment_page.fill_personal_details(last=candidate_data.last_name)
    if candidate_data.email:
        recruitment_page.fill_personal_details(email=candidate_data.email)

    recruitment_page.personal_info.click_save()
    alert = AlertErrorElement(browser)
    actual_alert_text = alert.get_input_field_text_alert()
    expected_alert_text = "Required"

    assert actual_alert_text == expected_alert_text, (
        f"Expected '{expected_alert_text}', but got '{actual_alert_text}'"
    )


@allure.title("Validate error message for an incorrectly formatted email")
def test_candidate_with_wrong_email_format(browser, login_as_admin):
    recruitment_page = login_as_admin
    recruitment_page.click_add_candidate()

    recruitment_page.fill_personal_details(first=fake.first_name())
    recruitment_page.fill_personal_details(last=fake.last_name())
    role_name = "Junior Account Assistant"
    recruitment_page.select_candidate(role_name)
    recruitment_page.fill_personal_details(email="test@")
    recruitment_page.personal_info.click_save()

    alert = AlertErrorElement(browser)
    actual_alert_text = alert.get_input_field_text_alert()
    expected_alert_text = "Expected format: admin@example.com"

    assert actual_alert_text == expected_alert_text, (
        f"Expected '{expected_alert_text}', but got '{actual_alert_text}'"
    )
