from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage
from config.config import config
from selenium.common.exceptions import TimeoutException

class BatchEditorPage(BasePage):
    ADD_COUNT_BUTTON = (By.XPATH, "//button[@data-id='add-count-button']")
    
    def __init__(self, driver):
        super().__init__(driver)
        self.url = f"{config.BASE_URL}/batch/20250813.U100053"
    
    def navigate_to_batch_editor(self):
        """Navigate to the specific batch editor page"""
        self.driver.get(self.url)
    
    def is_add_count_button_present(self, timeout: int = 10) -> bool:
        """Check if the add-count-button is present on the page"""
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(self.ADD_COUNT_BUTTON)
            )
            return True
        except TimeoutException:
            return False
    
    def wait_for_add_count_button(self, timeout: int = 10):
        """Wait for the add-count-button to be present and clickable"""
        wait = WebDriverWait(self.driver, timeout)
        return wait.until(EC.element_to_be_clickable(self.ADD_COUNT_BUTTON))
    
    def click_add_count_button(self):
        """Click the add-count-button if it's present"""
        if self.is_add_count_button_present():
            button = self.wait_for_add_count_button()
            button.click()
        else:
            raise TimeoutException("Add count button not found on the page")

    