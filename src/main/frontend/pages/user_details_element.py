import allure

from src.main.frontend.pages.base_page import BasePage


class UserDetailsElement(BasePage):
    FIRST_NAME_INPUT = (
        "//input[contains(@class, 'oxd-input') and translate(@placeholder, "
        "'ABCDEFGHIJKLMNOPQRSTUVWXYZ-', 'abcdefghijklmnopqrstuvwxyz ')='first name']"
    )
    MIDDLE_NAME_INPUT = (
        "//input[contains(@class, 'oxd-input') and translate(@placeholder, "
        "'ABCDEFGHIJKLMNOPQRSTUVWXYZ-', 'abcdefghijklmnopqrstuvwxyz ')='middle name']"
    )
    LAST_NAME_INPUT = (
        "//input[contains(@class, 'oxd-input') and translate(@placeholder, "
        "'ABCDEFGHIJKLMNOPQRSTUVWXYZ-', 'abcdefghijklmnopqrstuvwxyz ')='last name']"
    )
    EMAIL_INPUT = (
        "//div[label[text()='Email']]/following-sibling::div//input[contains(@class, 'oxd-input') "
        "and contains(@class, 'oxd-input--active')]"
    )
    SAVE_BUTTON = "//button[@type='submit' and contains(@class, 'oxd-button--secondary') and normalize-space(.)='Save']"
    CANCEL_BUTTON = "//button[@type='button' and contains(@class, 'oxd-button--ghost') and normalize-space(.)='Cancel']"

    @allure.step("Filling first name '{first_name}'")
    def fill_first_name(self, first_name: str) -> "UserDetailsElement":
        element = self.wait_for_element(self.FIRST_NAME_INPUT)
        if element:
            element.clear()
            element.send_keys(first_name)
            self.logger.info(f"Filled first name: '{first_name}'")
        else:
            self.logger.error("First name input field not found.")
        return self

    @allure.step("Filling middle name '{middle_name}'")
    def fill_middle_name(self, middle_name: str) -> "UserDetailsElement":
        element = self.wait_for_element(self.MIDDLE_NAME_INPUT)
        if element:
            element.clear()
            element.send_keys(middle_name)
            self.logger.info(f"Filled middle name: '{middle_name}'")
        else:
            self.logger.error("Middle name input field not found.")
        return self

    @allure.step("Filling last name '{last_name}'")
    def fill_last_name(self, last_name: str) -> "UserDetailsElement":
        element = self.wait_for_element(self.LAST_NAME_INPUT)
        if element:
            element.clear()
            element.send_keys(last_name)
            self.logger.info(f"Filled last name: '{last_name}'")
        else:
            self.logger.error("Last name input field not found.")
        return self

    @allure.step("Filling email '{email}'")
    def fill_email(self, email: str) -> "UserDetailsElement":
        element = self.wait_for_element(self.EMAIL_INPUT)
        if element:
            element.clear()
            element.send_keys(email)
            self.logger.info(f"Filled email: '{email}'")
        else:
            self.logger.error("Email input field not found.")
        return self

    @allure.step("Clicking save button")
    def click_save(self) -> "UserDetailsElement":
        element = self.wait_for_element(self.SAVE_BUTTON)
        if element:
            element.click()
            self.logger.info("Clicked save button.")
        else:
            self.logger.error("Save button not found.")
        return self

    @allure.step("Clicking cancel button")
    def click_cancel(self) -> "UserDetailsElement":
        element = self.wait_for_element(self.CANCEL_BUTTON)
        if element:
            element.click()
            self.logger.info("Clicked cancel button.")
        else:
            self.logger.error("Cancel button not found.")
        return self
