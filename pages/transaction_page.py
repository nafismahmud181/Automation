import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from pages.base_page import BasePage
from config.config import config
from selenium.common.exceptions import TimeoutException

class TransactionPage(BasePage):
    # Locators
    SEARCH_INPUT = (By.XPATH, "//*[@data-id='email-batches search id']")
    SEARCH_RESULTS = (By.XPATH, "//div[@class='search-results']")
    NO_RESULTS_MESSAGE = (By.XPATH, "//div[contains(text(),'No results found')]")

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

    def get_search_results(self, search_text=None):
        """
        Get search result text using the dynamic search text
        """
        try:
            if search_text:
                # Use the same dynamic XPath as is_search_successful
                dynamic_locator = (By.XPATH, f'//*[@data-id="email-batch {search_text} id"]')
                results = self.find_element(dynamic_locator)
                return results.text
            return ""
        except TimeoutException:
            return ""

    def is_no_results_displayed(self):
        """
        Check if no results message is displayed by finding .text-center class
        """
        try:
            no_results_locator = (By.CSS_SELECTOR, ".text-center")
            result = self.is_element_present(no_results_locator)
            time.sleep(5)  # Wait for 5 seconds after finding no results
            return result
        except TimeoutException:
            return False
    def is_search_successful(self, search_text=None):
        """
        Check if search was successful by verifying the element with dynamic search text is found
        """
        try:
            if search_text:
                # Dynamic XPath based on search text
                dynamic_locator = (By.XPATH, f'//*[@data-id="email-batch {search_text} id"]')
                return self.is_element_present(dynamic_locator)
            return self.is_element_present(self.SEARCH_RESULTS)
        except TimeoutException:
            return False