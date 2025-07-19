import os
import time
from datetime import datetime
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

class TestHelpers:
    @staticmethod
    def take_screenshot(driver, test_name: str) -> str:
        """Take screenshot and save with timestamp"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_dir = "screenshots"
        os.makedirs(screenshot_dir, exist_ok=True)
        
        filename = f"{screenshot_dir}/{test_name}_{timestamp}.png"
        driver.save_screenshot(filename)
        return filename
    
    @staticmethod
    def wait_for_element(driver, locator: tuple, timeout: int = 10):
        """Wait for element to be present and visible"""
        return WebDriverWait(driver, timeout).until(
            EC.visibility_of_element_located(locator)
        )
    
    @staticmethod
    def wait_for_element_clickable(driver, locator: tuple, timeout: int = 10):
        """Wait for element to be clickable"""
        return WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable(locator)
        )
    
    @staticmethod
    def clear_and_send_keys(element, text: str):
        """Clear element and send keys"""
        element.clear()
        element.send_keys(text)