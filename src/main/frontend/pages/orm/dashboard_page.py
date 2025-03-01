import allure
from selenium.common import NoSuchElementException

from src.main.frontend.pages.base_page import BasePage


class DashboardPage(BasePage):
    DASHBOARD_TITLES = "//div[@class='orangehrm-dashboard-widget-name']/p"

    @allure.step("Get list of available dashboards")
    def get_list_available_dashboards(self) -> list[str]:
        try:
            self.wait_for_element_to_be_clickable(self.DASHBOARD_TITLES)
            dashboards = self.get_items_elements(self.DASHBOARD_TITLES)
            return dashboards
        except NoSuchElementException as e:
            self.logger.warning(f"Error when trying to retrieve categories: {e}")
