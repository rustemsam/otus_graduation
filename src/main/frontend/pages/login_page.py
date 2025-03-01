import allure

from src.main.frontend.pages.base_page import BasePage


class LoginPage(BasePage):
    USERNAME_INPUT = "//input[@name='username']"
    PASSWORD_INPUT = "//input[@type='password']"
    LOGIN_BUTTON = "//button[@type='submit']"
    LOGIN_TITLE = "//h5[@class='oxd-text oxd-text--h5 orangehrm-login-title']"
    FORGOT_PASSWORD_BUTTON = "//div[@class='orangehrm-login-forgot']"

    def __init__(self, browser):
        super().__init__(browser)
        self.go_to_login_page()

    @allure.step("Going to login page")
    def go_to_login_page(self) -> None:
        try:
            url = self.browser.base_url
            self.browser.get(url)
            self.logger.info(f"Navigated to login page: {url}")
        except Exception as e:
            self.logger.error(f"Failed to navigate to the login page: {e}")

    @allure.step("Getting login title text")
    def get_login_title_text(self) -> str:
        element = self.wait_for_element(self.LOGIN_TITLE)
        if element:
            text = element.text
            self.logger.info(f"Login title text retrieved: '{text}'")
            return text
        else:
            self.logger.error("Login title did not appear within the timeout period.")
            return ""

    @allure.step("Filling username '{username}'")
    def fill_username(self, username: str) -> "LoginPage":
        element = self.wait_for_element(self.USERNAME_INPUT)
        if element:
            element.clear()
            element.send_keys(username)
            self.logger.info(f"Filled username: '{username}'")
        else:
            self.logger.error("Username input field not found.")
        return self

    @allure.step("Filling password '{password}'")
    def fill_password(self, password: str) -> "LoginPage":
        element = self.wait_for_element(self.PASSWORD_INPUT)
        if element:
            element.clear()
            element.send_keys(password)
            self.logger.info("Filled password.")
        else:
            self.logger.error("Password input field not found.")
        return self

    @allure.step("Clicking for login")
    def click_for_login(self) -> "LoginPage":
        element = self.wait_for_element(self.LOGIN_BUTTON)
        if element:
            element.click()
            self.logger.info("Clicked the login button.")
        else:
            self.logger.error("Login button not found.")
        return self

    @allure.step("Clicking login to admin panel")
    def login_to_admin_panel(self, username: str, password: str) -> None:
        self.fill_username(username).fill_password(password).click_for_login()

    @allure.step("Clicking forgot password")
    def forgot_password(self) -> None:
        element = self.wait_for_element_to_be_clickable(self.FORGOT_PASSWORD_BUTTON)
        if element:
            element.click()
            self.logger.info("Clicked the forgot password button.")
        else:
            self.logger.error("Forgot password button not found or not clickable.")
