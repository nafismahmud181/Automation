from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from config.config import config

class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, config.EXPLICIT_WAIT)
    
    def find_element(self, locator: tuple):
        """Find element with explicit wait"""
        return self.wait.until(EC.visibility_of_element_located(locator))
    
    def find_clickable_element(self, locator: tuple):
        """Find clickable element with explicit wait"""
        return self.wait.until(EC.element_to_be_clickable(locator))
    
    def is_element_present(self, locator: tuple, timeout: int = 5) -> bool:
        """Check if element is present"""
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
            return True
        except TimeoutException:
            return False
    
    def get_text(self, locator: tuple) -> str:
        """Get text from element"""
        element = self.find_element(locator)
        return element.text
    
    def click(self, locator: tuple):
        """Click on element"""
        element = self.find_clickable_element(locator)
        element.click()
    
    def send_keys(self, locator: tuple, text: str):
        """Send keys to element"""
        element = self.find_element(locator)
        element.clear()
        element.send_keys(text)
    
    def get_current_url(self) -> str:
        """Get current page URL"""
        return self.driver.current_url
    
    def get_page_title(self) -> str:
        """Get page title"""
        return self.driver.title