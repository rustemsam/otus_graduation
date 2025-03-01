import allure
from selenium.common.exceptions import NoSuchElementException

from src.main.frontend.pages.base_page import BasePage


class AlertErrorElement(BasePage):
    FAILURE_ALERT = "//div[@class='oxd-alert-content oxd-alert-content--error']"
    INPUT_FIELD_ALERT = "//span[@class='oxd-text oxd-text--span oxd-input-field-error-message oxd-input-group__message']"

    def _get_alert_text(self, locator: str, timeout: int, alert_name: str) -> str:
        """
        Utility method to wait for an alert element, retrieve its text, and handle exceptions.

        :param locator: The XPath locator for the alert element.
        :param timeout: Maximum time to wait for the element.
        :param alert_name: A descriptive name for logging purposes.
        :return: The text of the alert element or an empty string if not found.
        """
        try:
            alert_element = self.wait_for_element(locator, timeout=timeout)
            return alert_element.text
        except NoSuchElementException:
            self.logger.info(f"{alert_name} did not appear within the timeout period.")
            return ""

    @allure.step("Getting failure text alert")
    def get_failure_text_alert(self) -> str:
        return self._get_alert_text(
            self.FAILURE_ALERT, timeout=10, alert_name="Failure alert"
        )

    @allure.step("Getting input text alert")
    def get_input_field_text_alert(self) -> str:
        return self._get_alert_text(
            self.INPUT_FIELD_ALERT, timeout=10, alert_name="Input field alert"
        )
