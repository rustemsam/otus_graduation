import time

import allure
from selenium.common import NoSuchElementException

from src.main.frontend.pages.base_page import BasePage
from src.main.frontend.pages.user_details_element import UserDetailsElement


class PimPage(BasePage):
    PIM = "//a[contains(@class, 'oxd-main-menu-item') and contains(@href, '/web/index.php/pim/viewPimModule')]"
    EMPLOYEE_NAME_INPUT = "///label[text()='Employee Name']/ancestor::div[contains(@class, 'oxd-input-group')]//input"
    EMPLOYEE_ID_INPUT = "//label[text()='Employee Id']/ancestor::div[contains(@class, 'oxd-input-group')]//input"
    USERNAME_LOGIN_INPUT = "//label[normalize-space(text())='Username']/ancestor::div[contains(@class, 'oxd-input-group')]//input"
    PASSWORD_LOGIN_INPUT = "//label[normalize-space(text())='Password']/ancestor::div[contains(@class, 'oxd-input-group')]//input"
    CONFIRM_PASSWORD_LOGIN_INPUT = "//label[normalize-space(text())='Confirm Password']/ancestor::div[contains(@class, 'oxd-input-group')]//input"
    EMPLOYMENT_STATUS_SELECTOR = "//label[normalize-space(text())='Employment Status']/ancestor::div[contains(@class, 'oxd-input-group')]//div[contains(@class, 'oxd-select-text-input') and @tabindex='0']"
    SUPERVISOR_NAME_INPUT = "//label[text()='Supervisor Name']/ancestor::div[contains(@class, 'oxd-input-group')]//input"
    SEARCH_BUTTON = "//button[@type='submit' and contains(@class, 'oxd-button--secondary') and normalize-space(.)='Search']"
    ADD_BUTTON = "//button[@type='button' and contains(@class, 'oxd-button--secondary') and .//i[contains(@class, 'bi-plus')] and contains(normalize-space(.), 'Add')]"
    CREATE_LOGIN_DETAILS_BUTTON = "//span[contains(@class, 'oxd-switch-input') and contains(@class, 'oxd-switch-input--active') and contains(@class, '--label-right')]"
    PIM_PERSONAL_TITLE = "//h6[contains(@class, 'orangehrm-main-title')]"
    TABLE_ROWS = "//div[contains(@class, 'oxd-table-body')]//div[@role='row' and contains(@class, 'oxd-table-row--clickable')]"

    def __init__(self, browser):
        super().__init__(browser)
        self.personal_info = UserDetailsElement(browser)
        self.click_pim()

    @allure.step("Clicking pim section")
    def click_pim(self):
        try:
            self.browser.refresh()
            self.wait_for_element(self.PIM, 3).click()
            self.wait_for_element(self.PIM, 3).click()
            self.browser.refresh()
        except NoSuchElementException as e:
            print(f"Error when trying to click the pim button: {e}")
            self.logger.error(f"Click on PIM failed: {e}")
            screenshot_path = f"error_screenshot_{int(time.time())}.png"
            self.browser.save_screenshot(screenshot_path)
            self.logger.info(f"Screenshot saved to {screenshot_path}")
        return self

    @allure.step("Selecting employment status '{status}'")
    def select_employment_status(self, status):
        employment_status = f"//div[@role='option' and contains(@class, 'oxd-select-option') and span[text()='{status}']]"
        try:
            self.wait_for_element_to_be_clickable(
                self.EMPLOYMENT_STATUS_SELECTOR
            ).click()
            self.wait_for_element(employment_status).click()
        except NoSuchElementException as e:
            print(f"Error when trying to click the employment status button: {e}")
        return self

    @allure.step("Clicking search button")
    def click_search(self):
        try:
            self.wait_for_element(self.SEARCH_BUTTON).click()
        except NoSuchElementException as e:
            print(f"Error when trying to click search button: {e}")
        return self

    @allure.step("Clicking add button")
    def click_add_button(self):
        try:
            self.wait_for_element(self.ADD_BUTTON).click()
        except NoSuchElementException as e:
            print(f"Error when trying to click add button: {e}")
        return self

    @allure.step("Clicking create login details button")
    def click_create_login_details_button(self):
        try:
            self.wait_for_element(self.CREATE_LOGIN_DETAILS_BUTTON).click()
        except NoSuchElementException as e:
            print(f"Error when trying to click add button: {e}")
        return self

    @allure.step(
        "Filling login details: username '{username}', password '{password}', confirm password '{confirm_password}'"
    )
    def fill_login_details(self, username, password, confirm_password):
        try:
            input_username = self.wait_for_element(self.USERNAME_LOGIN_INPUT)
            input_username.clear()
            input_username.send_keys(username)

            input_password = self.wait_for_element(self.PASSWORD_LOGIN_INPUT)
            input_password.clear()
            input_password.send_keys(password)

            input_confirm_password = self.wait_for_element(
                self.CONFIRM_PASSWORD_LOGIN_INPUT
            )
            input_confirm_password.clear()
            input_confirm_password.send_keys(confirm_password)
        except NoSuchElementException as e:
            print(f"Error when trying to fill login details: {e}")
        return self

    @allure.step("Get list of available pim records")
    def get_list_available_pim_records(self) -> list[str] | None:
        try:
            self.wait_for_element_to_be_clickable(self.TABLE_ROWS)
            pim_rows = self.get_items_elements(self.TABLE_ROWS)
            return pim_rows
        except NoSuchElementException as e:
            self.logger.warning(f"Error when trying to retrieve categories: {e}")

    @allure.step(
        "Filling personal  details: first name '{first}', last name '{last}', middle name '{middle}'"
    )
    def fill_personal_details(self, first=None, last=None, middle=None):
        if first:
            self.personal_info.fill_first_name(first)
        if last:
            self.personal_info.fill_last_name(last)
        if middle:
            self.personal_info.fill_middle_name(middle)

    @allure.step("Getting pim title")
    def get_pim_title(self) -> str:
        self.wait_for_page_load()
        expected_url_part = "/viewPersonalDetails/empNumber/"
        if not self.wait_for_url_to_contain(expected_url_part):
            return ""
        try:
            application_stage = self.wait_for_element(self.PIM_PERSONAL_TITLE)
            return application_stage.text
        except NoSuchElementException:
            self.logger.info("PIM title did not appear within the timeout period.")
