import allure

from src.main.frontend.pages.base_page import BasePage


class PasswordResetPage(BasePage):
    USERNAME_INPUT = "//input[@name='username']"
    RESET_BUTTON = "//button[@type='submit']"
    CANCEL_BUTTON = "//button[@type='button']"
    CONFIRMATION_OF_RESETTING_PASSWORD = (
        "//h6[@class='oxd-text oxd-text--h6 orangehrm-forgot-password-title']"
    )

    @allure.step("Filling username '{username}'")
    def fill_username(self, username: str) -> "PasswordResetPage":
        element = self.wait_for_element(self.USERNAME_INPUT)
        if element:
            element.clear()
            element.send_keys(username)
            self.logger.info(f"Filled username: '{username}'")
        else:
            self.logger.error(
                "Username input field not found when trying to fill username."
            )
        return self

    @allure.step("Clicking reset password")
    def click_reset_password(self) -> "PasswordResetPage":
        element = self.wait_for_element(self.RESET_BUTTON)
        if element:
            element.click()
            self.logger.info("Clicked the reset password button.")
        else:
            self.logger.error("Reset password button not found.")
        return self

    @allure.step("Clicking cancel button")
    def click_cancel(self) -> "PasswordResetPage":
        element = self.wait_for_element(self.CANCEL_BUTTON)
        if element:
            element.click()
            self.logger.info("Clicked the cancel button.")
        else:
            self.logger.error("Cancel button not found.")
        return self

    @allure.step("Resetting password for '{username}'")
    def reset_password(self, username: str) -> "PasswordResetPage":
        self.fill_username(username).click_reset_password()
        return self

    @allure.step("Getting reset password confirmation")
    def get_reset_password_confirmation(self) -> str:
        element = self.wait_for_element(self.CONFIRMATION_OF_RESETTING_PASSWORD)
        if element:
            confirmation_text = element.text
            self.logger.info(
                f"Reset password confirmation retrieved: '{confirmation_text}'"
            )
            return confirmation_text
        else:
            self.logger.error(
                "Confirmation text did not appear within the timeout period."
            )
            return ""
