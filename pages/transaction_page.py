from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from pages.base_page import BasePage
from config.config import config
from selenium.common.exceptions import TimeoutException

class TransactionPage(BasePage):
    # Locators
    SEARCH_INPUT = (By.XPATH, "//*[@data-id='email-batches search id']")  # Update this xpath based on your actual page
    SEARCH_RESULTS = (By.XPATH, "//div[@class='search-results']")  # Update this xpath based on your actual page
    NO_RESULTS_MESSAGE = (By.XPATH, "//div[contains(text(),'No results found')]")  # Update this xpath

    def __init__(self, driver):
        super().__init__(driver)
        self.url = f"{config.BASE_URL}/"  # Main page URL after successful login

    def search_text(self, text: str):
        """
        Enter text in search box and press Enter
        """
        search_box = self.find_element(self.SEARCH_INPUT)
        search_box.clear()
        search_box.send_keys(text)
        search_box.send_keys(Keys.RETURN)

    def get_search_results(self):
        """
        Get all search results
        """
        try:
            results = self.find_element(self.SEARCH_RESULTS)
            return results.text
        except TimeoutException:
            return ""

    def is_no_results_displayed(self):
        """
        Check if no results message is displayed
        """
        try:
            return self.is_element_present(self.NO_RESULTS_MESSAGE)
        except TimeoutException:
            return False

    def is_search_successful(self):
        """
        Check if search was successful by verifying results are displayed
        """
        try:
            return self.is_element_present(self.SEARCH_RESULTS)
        except TimeoutException:
            return False
