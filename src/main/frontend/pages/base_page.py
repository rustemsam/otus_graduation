import logging
import os
from typing import List, Optional

from selenium.common.exceptions import (
    NoSuchElementException,
    StaleElementReferenceException,
    TimeoutException,
)
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


class BasePage:
    DEFAULT_TIMEOUT = 10
    JS_ARGUMENT_CLICK = "arguments[0].click();"
    JS_ARGUMENT_SCROLL = "arguments[0].scrollIntoView(true);"

    def __init__(self, browser: WebDriver):
        """
        Initialize the BasePage with a Selenium WebDriver instance.
        """
        self.browser = browser
        self.__config_logger()

    def __config_logger(self, to_file: bool = False) -> None:
        """
        Configures the logger for the page.
        If to_file is True, logs will be saved to a file named based on the browser's test name.
        """
        self.logger = logging.getLogger(self.__class__.__name__)
        os.makedirs("logs", exist_ok=True)
        if not self.logger.handlers:
            if to_file:
                self.logger.addHandler(
                    logging.FileHandler(
                        f"logs/{getattr(self.browser, 'test_name', 'default')}.log"
                    )
                )
            self.logger.setLevel(getattr(self.browser, "log_level", logging.INFO))

    def input_value(self, locator: str, value: str) -> None:
        """
        Finds an element by the provided locator, clears its content, and inputs the given value.
        """
        self.logger.info(
            f"Inputting value '{value}' into element with locator: {locator}"
        )
        element = self.wait_for_element(locator)
        if element:
            element.clear()
            element.send_keys(value)
        else:
            self.logger.error(
                f"Element with locator '{locator}' not found to input value."
            )

    def get_items_elements(self, xpath_locator: str) -> List[str]:
        """
        Retrieves and returns a list of non-empty text strings from all elements matching the given XPath locator.
        """
        try:
            elements = self.browser.find_elements(By.XPATH, xpath_locator)
            self.logger.info(
                f"Found {len(elements)} items matching locator '{xpath_locator}'."
            )
            return [el.text.strip() for el in elements if el.text.strip()]
        except (NoSuchElementException, StaleElementReferenceException) as e:
            self.logger.error(f"No available text from elements '{xpath_locator}': {e}")
            return []

    def get_text(self, path: str, locator: By = By.XPATH) -> str:
        """
        Returns the text from a single element identified by the locator and path.
        If the element is not found, returns an empty string.
        """
        try:
            element = self.browser.find_element(locator, path)
            text = element.text.strip()
            self.logger.info(
                f"Retrieved text '{text}' from element with locator '{path}'."
            )
            return text
        except (NoSuchElementException, StaleElementReferenceException) as e:
            self.logger.error(
                f"No available text from element '{path}' using locator {locator}: {e}"
            )
            return ""

    def _wait_with_timeout(self, timeout: int) -> WebDriverWait:
        """
        Returns a WebDriverWait instance with the specified timeout.
        """
        return WebDriverWait(self.browser, timeout)

    def wait_for_page_load(self, timeout: int = DEFAULT_TIMEOUT) -> None:
        """
        Waits until the page has completely loaded by checking the document.readyState.
        """
        WebDriverWait(self.browser, timeout).until(
            lambda driver: driver.execute_script("return document.readyState")
            == "complete"
        )

    def wait_for_url_to_contain(
        self, partial_url: str, timeout: int = DEFAULT_TIMEOUT
    ) -> bool:
        """
        Waits for the current URL to contain the given substring.
        Returns True if found, False if the timeout is reached.
        """
        try:
            WebDriverWait(self.browser, timeout).until(EC.url_contains(partial_url))
            self.logger.info(f"URL contains '{partial_url}'. Proceeding...")
            return True
        except TimeoutException as e:
            self.logger.error(
                f"Expected URL containing '{partial_url}' did not load within {timeout} seconds: {e}"
            )
            return False

    def wait_for_element(
        self, xpath: str, timeout: int = DEFAULT_TIMEOUT
    ) -> Optional[WebElement]:
        """
        Waits for an element to be visible on the page using its XPath locator.
        Returns the WebElement if found, or None if not found within the timeout.
        """
        try:
            self.wait_for_page_load()
            wait = self._wait_with_timeout(timeout)
            element = wait.until(EC.visibility_of_element_located((By.XPATH, xpath)))
            return element
        except TimeoutException as e:
            self.logger.error(
                f"Element with locator '{xpath}' was not found within {timeout} seconds: {e}"
            )
            return None

    def wait_for_element_to_be_clickable(
        self, xpath: str, timeout: int = DEFAULT_TIMEOUT
    ) -> Optional[WebElement]:
        """
        Waits for an element to be clickable.
        Returns the WebElement if clickable, or None if the timeout is reached.
        """
        try:
            wait = self._wait_with_timeout(timeout)
            element = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
            return element
        except TimeoutException as e:
            self.logger.error(
                f"Element with locator '{xpath}' was not clickable within {timeout} seconds: {e}"
            )
            return None

    def wait_for_new_page_loaded(
        self, url: str, timeout: int = DEFAULT_TIMEOUT
    ) -> bool:
        """
        Waits for a new page to load by checking if the current URL contains the given substring.
        Returns True if the new page loads, otherwise returns False.
        """
        try:
            wait = self._wait_with_timeout(timeout)
            result = wait.until(EC.url_contains(url))
            return result
        except TimeoutException as e:
            self.logger.warning(
                f"Page did not load with URL containing '{url}' within {timeout} seconds: {e}"
            )
            return False

    def wait_for_element_to_disappear(
        self, xpath: str, timeout: int = DEFAULT_TIMEOUT
    ) -> bool:
        """
        Waits for an element to disappear from the page.
        Returns True if the element disappears within the timeout, otherwise returns False.
        """
        try:
            wait = self._wait_with_timeout(timeout)
            element = wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
            wait.until(EC.invisibility_of_element(element))
            self.logger.info(f"Element with locator '{xpath}' disappeared.")
            return True
        except TimeoutException as e:
            self.logger.warning(
                f"Element with locator '{xpath}' didn't disappear within {timeout} seconds: {e}"
            )
            return False

    def scroll_to_element(self, element: WebElement) -> None:
        """
        Scrolls the page until the specified element is in view.
        """
        self.logger.info(f"Scrolling to element: {element}.")
        self.browser.execute_script(self.JS_ARGUMENT_SCROLL, element)

    def js_click_to_element(self, element: WebElement) -> None:
        """
        Clicks on an element using JavaScript.
        """
        self.logger.info(f"Clicking element via JS: {element}.")
        self.browser.execute_script(self.JS_ARGUMENT_CLICK, element)

    def maximize_browser_window(self) -> None:
        """
        Maximizes the browser window.
        """
        self.logger.info("Maximizing browser window.")
        self.browser.maximize_window()

    def click_using_action(self, locator: str) -> None:
        """
        Clicks an element using ActionChains for a more robust interaction.
        """
        self.logger.info(
            f"Clicking element using ActionChains with locator '{locator}'."
        )
        element = self.wait_for_element(locator)
        if element:
            actions = ActionChains(self.browser)
            actions.move_to_element(element).click().perform()
        else:
            self.logger.error(
                f"Element with locator '{locator}' not found for clicking using ActionChains."
            )
