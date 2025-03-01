import platform

import allure
from selenium.common import NoSuchElementException
from selenium.webdriver import Keys

from src.main.frontend.pages.base_page import BasePage
from src.main.frontend.pages.user_details_element import UserDetailsElement


class RecruitmentPage(BasePage):
    RECRUITMENT = "//a[contains(@class, 'oxd-main-menu-item') and contains(@href, '/web/index.php/recruitment/viewRecruitmentModule')]"
    ADD_CANDIDATE_BUTTON = "//button[contains(@class, 'oxd-button') and contains(@class, 'oxd-button--secondary') and contains(., 'Add')]"
    VACANCY_SELECTOR = "//i[contains(@class, 'oxd-icon') and contains(@class, 'bi-caret-down-fill') and contains(@class, 'oxd-select-text--arrow')]"
    DATE_OF_APPLICATION_INPUT = "//div[label[text()='Date of Application']]/following-sibling::div//input[contains(@class, 'oxd-input')]"
    CONSENT_CHECKBOX = (
        "//label[contains(@class, 'oxd-label') and text()='Consent to keep data']"
    )
    SAVE_BUTTON = "//button[contains(@class, 'oxd-button') and text()=' Save ']"
    APPLICATION_STAGE_TITLE = "//h6[contains(@class, 'oxd-text') and contains(@class, 'orangehrm-main-title')]"

    def __init__(self, browser):
        super().__init__(browser)
        self.personal_info = UserDetailsElement(browser)
        self.click_recruitment()

    @allure.step(
        "Filling personal  details: first name '{first}', last name '{last}', middle name '{middle}', email '{email}'"
    )
    def fill_personal_details(self, first=None, last=None, middle=None, email=None):
        if first:
            self.personal_info.fill_first_name(first)
        if last:
            self.personal_info.fill_last_name(last)
        if middle:
            self.personal_info.fill_middle_name(middle)
        if email:
            self.personal_info.fill_email(email)

    @allure.step("Clicking recruitment section")
    def click_recruitment(self):
        try:
            self.wait_for_element(self.RECRUITMENT).click()
        except NoSuchElementException as e:
            print(f"Error when trying to click the recruitment button: {e}")
        return self

    @allure.step("Clicking add candidate")
    def click_add_candidate(self):
        try:
            self.wait_for_element(self.ADD_CANDIDATE_BUTTON).click()
        except NoSuchElementException as e:
            print(f"Error when trying to click the add candidate button: {e}")
        return self

    @allure.step("Clicking select candidate")
    def select_candidate(self, role):
        vacancy_input = (
            f"//div[contains(@class, 'oxd-select-option') and span[text()='{role}']]"
        )
        try:
            self.wait_for_element_to_be_clickable(self.VACANCY_SELECTOR).click()
            self.wait_for_element(vacancy_input).click()
        except NoSuchElementException as e:
            print(f"Error when trying to click the add candidate button: {e}")
        return self

    @allure.step("Filling application date '{application_date}'")
    def fill_application_date(self, application_date: str):
        try:
            input_application_date = self.wait_for_element(
                self.DATE_OF_APPLICATION_INPUT
            )

            input_application_date.click()
            select_all_keys = (
                Keys.COMMAND if platform.system() == "Darwin" else Keys.CONTROL
            )
            input_application_date.send_keys(select_all_keys + "a")
            input_application_date.send_keys(select_all_keys + "a")
            input_application_date.send_keys(Keys.BACKSPACE)
            input_application_date.send_keys(Keys.DELETE)
            input_application_date.send_keys(application_date)

        except NoSuchElementException as e:
            print(f"Error when trying to fill application date: {e}")

        return self

    @allure.step("Clicking consent checkbox")
    def click_consent_checkbox(self):
        try:
            self.wait_for_element(self.CONSENT_CHECKBOX).click()
        except NoSuchElementException as e:
            print(f"Error when trying to click consent checkbox: {e}")
        return self

    @allure.step("Getting application stage title")
    def get_application_stage_title(self) -> str:
        self.wait_for_page_load()
        expected_url_part = "/recruitment/addCandidate/"
        if not self.wait_for_url_to_contain(expected_url_part):
            return ""

        try:
            application_stage = self.wait_for_element(self.APPLICATION_STAGE_TITLE)
            return application_stage.text
        except NoSuchElementException:
            self.logger.info("Failure alert did not appear within the timeout period.")
